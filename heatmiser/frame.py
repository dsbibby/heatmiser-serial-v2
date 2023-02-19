import math
from heatmiser.logging import log


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
        except IndexError as error:
            print(error)

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
