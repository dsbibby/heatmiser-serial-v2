import asyncio
import math
from heatmiser.logging import log
from datetime import datetime, timedelta


class HeatmiserProtocol(asyncio.Protocol):
    def __init__(self, queue):
        super().__init__()
        self.transport = None
        self.queue = queue
        self._lastwrite = None

    def connection_made(self, transport):
        self.transport = transport
        log('debug', 'port opened', transport)
        # You can manipulate Serial object via transport
        transport.serial.rts = False

    def data_received(self, data):
        frame = HeatmiserFrame(data=data)
        asyncio.ensure_future(self.queue.put(frame))
        self._lastwrite = None

    def connection_lost(self, exc):
        log('debug', 'port closed')
        #self.transport.loop.stop()

    def pause_writing(self):
        log('debug', 'pause writing')
        log('debug', self.transport.get_write_buffer_size())

    def resume_writing(self):
        log('debug', self.transport.get_write_buffer_size())
        log('debug', 'resume writing')

    async def write_frame(self, frame):
        if self._lastwrite:
            start = datetime.now()
            log('debug1', 'write delayed awaiting previous rx')
            while self._lastwrite and \
                    self._lastwrite + timedelta(seconds=2) > datetime.now():
                await asyncio.sleep(0.1)
            log('debug1', 'waited', (datetime.now() - start).seconds,
                'seconds before writing')
        log('debug1', "writing frame:", frame)
        self.transport.write(frame.data)
        self._lastwrite = datetime.now()


class HeatmiserFrame:
    def __init__(self, device_id=None, command_code=None, data=None):
        if device_id and command_code:
            self._data = bytearray(4)
            self.set_bytes(0, device_id)
            self.set_bytes(1, command_code)
            if data:
                self.set_bytes(2, data)
        elif isinstance(data, bytes):
            self._data = bytearray(data)
        else:
            raise TypeError


    def __str__(self):
        return ":".join("{:02x}".format(c) for c in self._data)

    def get_bytes(self, index, length=1) -> bytes:
        try:
            return bytes(self._data[index:index+length])
        except IndexError as e:
            print(e)

    def set_bytes(self, index, value, length=1):
        value = value.to_bytes(length, 'big')
        flength = index + length
        log('debug1', "frame length:", len(self._data), "- target length:",
            flength, "- index:", index)
        if flength >= len(self._data):
            self._data += bytearray(flength - len(self._data) + 1)

        self._data[index:flength] = value
        # update checksum
        self._data[-1] = self.checksum

    def get_int(self, byte_index, byte_length=1) -> int:
        return int.from_bytes(self.get_bytes(byte_index, byte_length), 'big')

    def get_bits(self, start_byte, start_bit, length=1):
        byte_count = math.ceil((start_bit + length) / 8)
        data = self.get_int(start_byte, byte_count)
        length_mask = (1 << length) - 1
        return data >> start_bit & length_mask

    def get_bool(self, byte, bit, length=1):
        data = self.get_bits(byte, bit, length)
        if length == 1:
            return data == 1
        else:
            return [bool(data & (1 << n)) for n in range(length)]

    @property
    def device_id(self):
        return self.get_int(0)

    @property
    def command_code(self):
        return self.get_int(1)

    @property
    def is_valid(self):
        # print("calc_sum is", "{:02x}".format(chksum))
        return self.checksum == self._data[-1]

    @property
    def checksum(self):
        return sum(self._data[:-1]) & 0xFF

    @property
    def data(self):
        return self._data
