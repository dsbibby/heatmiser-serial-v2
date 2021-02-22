import asyncio
import math
#import serial_asyncio


class HeatmiserProtocol(asyncio.Protocol):
    def __init__(self, queue):
        super().__init__()
        self.transport = None
        self.queue = queue

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
       #transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        frame = HeatmiserFrame(data=data)
        asyncio.ensure_future(self.queue.put(frame))

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')
        
    def write_frame(self, frame):
        print("writing frame:", frame)
        self.transport.write(frame.data)


class HeatmiserFrame:
    def __init__(self, device_id=None, command_code=None, data=None):
        if device_id and command_code:
            self.data = bytearray(4)
            self.set_bytes(0, device_id)
            self.set_bytes(1, command_code)
            if data:
                self.set_bytes(2, data)
        elif isinstance(data, bytes):
            self.data = bytearray(data)
        else:
            raise TypeError

    def __str__(self):
        return ":".join("{:02x}".format(c) for c in self.data)

    def get_bytes(self, index, length=1) -> bytes:
        try:
            return bytes(self.data[index:index+length])
        except IndexError as e:
            print(e)
    
    def set_bytes(self, index, value, length=1):
        value = value.to_bytes(length, 'big')
        flength = index + length
        # print("frame length:", len(self.data), "- target length:", flength, "- index:", index)
        if flength >= len(self.data):
            self.data += bytearray(flength - len(self.data) + 1)
        
        self.data[index:flength] = value
        # upsate checksum
        self.data[-1] = self.checksum
    
    def get_int(self, byte_index, byte_length=1) -> int:
        return int.from_bytes(self.get_bytes(byte_index, byte_length), 'big')
        
    def get_bits(self, start_byte, start_bit, length=1):
        byte_count = math.ceil((start_bit + length) / 8)
        data = self.get_int(start_byte, byte_count)
        length_mask = (1 << length) - 1
        return data >> start_bit & length_mask
        
    def get_bool(self, byte, bit):
        return self.get_bits(byte, bit) == 1
        
    @property
    def device_id(self):
        return self.get_int(0)

    @property  
    def command_code(self):
        return self.get_int(1)
        
    @property
    def is_valid(self):
        #print("calc_sum is", "{:02x}".format(chksum))
        return self.checksum == self.data[-1]

    @property
    def checksum(self):
        return sum(self.data[:-1]) & 0xFF