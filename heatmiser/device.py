from heatmiser.protocol import HeatmiserFrame
from heatmiser.logging import log
from datetime import datetime, timedelta


class HeatmiserDevice:
    C_READ_PARAM = 0x00
    TYPE_STR = "Unknown"
    MONITOR_PARAMS = [
        "datetime", "room_temp", "set_temp", "part_number",
        "switching_diff", "temp_format", "heating_state",
        "lock_state", "frost_mode", "enabled", "set_temp",
        "frost_temp", "output_delay", "floor_temp"]
    on_param_change = None

    def __init__(self, frame: HeatmiserFrame = None):
        self.__dict__["_params"] = {}
        self._id = None
        for param in self.MONITOR_PARAMS:
            self._params[param] = None
        if frame:
            self._declare(frame)


    """Perform initial setup of the device from a discover frame (0x4d)
    """
    def _declare(self, frame: HeatmiserFrame):
        if not frame.is_valid:
            log('warn', "invalid frame:", frame)
            return

        self._id = frame.device_id
        command = frame.command_code

        if command == 0x4d:
            type = frame.get_int(2)
            if type == 0x51:
                if not isinstance(self, HeatmiserDevicePRT):
                    self.__class__ = HeatmiserDevicePRT
                    self.__init__(frame)
            elif type == 0x52:
                if not isinstance(self, HeatmiserDevicePRTHW):
                    self.__class__ = HeatmiserDevicePRTHW
                    self.__init__(frame)
            # self.room_temp = frame.get_int(3) - 0x50
            # self.set_temp = frame.get_int(4) - 0x50
        else:
            log('error', "expected command code 0x4d")

    """Update the device with current data
    """
    def handle_frame(self, frame: HeatmiserFrame):
        if not frame.is_valid or frame.device_id != self.id:
            log('error', "Invalid frame for device_id", self.id, ":", frame)
        if frame.command_code == self.C_READ_PARAM:
            now = datetime.now()
            weekday = frame.get_bits(3, 0, 4) - 1
            hour, minute, self._room_temp = frame.get_bytes(4, 3)
            self._datetime = self._relative_date(now, weekday, hour, minute)
            self._part_number = frame.get_bits(7, 0, 4)
            self._switching_diff = frame.get_bits(7, 4, 4)
            self._temp_format = frame.get_bool(8, 0)
            self._manual_hw_state, self._hw_state, self._heating_state, \
                self._frost_mode, self._lock_state, self._enabled \
                = frame.get_bool(8, 2, 6)
            self._set_temp, self._frost_temp, self._output_delay, \
                self._floor_temp = frame.get_bytes(9, 4)

    def _relative_date(self, reference, weekday, hour, minute):
        if reference.weekday() < weekday:
            weekday -= 7
        days = reference.weekday() - weekday
        return (reference - timedelta(days=days)).replace(
            hour=int(hour), minute=int(minute), second=0, microsecond=0)

    def _send_param_update(self, name, value):
        log('debug', f'sending update to param {name}: {value}')

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
        if name.startswith("_") and name[1:] in self._params:
            name = name[1:]
            if self._params[name] != value:
                self._params[name] = value
                if callable(self.on_param_change):
                    self.on_param_change(name, value)
        elif name in self._params:
            self._send_param_update(name, value)
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return (f'ID: {self.id}, Type: {self.TYPE_STR}, '
            f'Room Temp: {self.room_temp}, State: {self.enabled}')


class HeatmiserDevicePRT(HeatmiserDevice):
    C_READ_PARAM = 0x26
    TYPE_STR = "PRT"


class HeatmiserDevicePRTHW(HeatmiserDevice):
    C_READ_PARAM = 0x29
    TYPE_STR = "PRTHW"

    def __init__(self, frame: HeatmiserFrame = None):
        super().__init__(frame)
        self._params["manual_hw_state"] = None
        self._params["hw_state"] = None
