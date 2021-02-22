from heatmiser import protocol

class HeatmiserDevice:
    C_READ_PARAM = 0x00
    TYPE_STR = "Unknown"
    PARAMS = ["state", "room_temp", "set_temp"]
    on_param_change = None
    
    
    def __init__(self, frame: protocol.HeatmiserFrame = None):
        self.__dict__["_params"] = {}
        self._id = None
        for param in self.PARAMS:
            self._params[param] = None
        print(self._params)
        if frame:
            self._declare(frame)

    """Perform initial setup of the device from a discover frame (0x4d)
    """
    def _declare(self, frame: protocol.HeatmiserFrame):
        if not frame.is_valid:
            print("invalid frame:", frame)
            return
        
        self._id = frame.device_id
        command = frame.command_code

        if command == 0x4d:
            type = frame.get_int(2)
            if type == 0x51:
                self.__class__ = HeatmiserDevicePRT
            elif type == 0x52:
                self.__class__ = HeatmiserDevicePRTHW
            self.room_temp = frame.get_int(3) - 0x50
            self.set_temp = frame.get_int(4) - 0x50
        else:
            print("expected command code 0x4d")

    """Update the device with current data
    """
    def handle_frame(self, frame: protocol.HeatmiserFrame):
        if not frame.is_valid or frame.device_id != self.id:
            print("Invalid frame for device_id", self.id, ":", frame)
        if frame.command_code == self.C_READ_PARAM:
            self.state = frame.get_bool(8, 7)

    @property
    def id(self) -> int:
        return self._id
    
    def __getattr__(self, name):
        def get_param():
            try:
                return self._params[name]
            except KeyError:
                raise AttributeError
        return get_param()
    
    def __setattr__(self, name, value):
        if name in self._params:
            if self._params[name] != value:
                self._params[name] = value
                if callable(self.on_param_change):
                    self.on_param_change(name, value)
        else:
            object.__setattr__(self, name, value)
            
    def __str__(self):
        return f'ID: {self.id}, Type: {self.TYPE_STR}, Room Temp: {self.room_temp}, State: {self.state}'


class HeatmiserDevicePRT(HeatmiserDevice):
    C_READ_PARAM = 0x26
    TYPE_STR = "PRT"


class HeatmiserDevicePRTHW(HeatmiserDevice):
    C_READ_PARAM = 0x29
    TYPE_STR = "PRTHW"
    