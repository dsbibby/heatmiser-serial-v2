import asyncio
from heatmiser.protocol import HeatmiserFrame
from heatmiser.logging import log
from datetime import datetime, timedelta


class HeatmiserDevice():
    C_READ_PARAM = 0x00
    C_WRITE_PARAM = 0x00
    MODEL_CODE = 0x00
    TYPE_STR = "Unknown"

    MONITOR_PARAMS = {
        "datetime": None,
        "room_temp": 0x08,
        "set_temp": 0x04,
        "part_number": None,
        "switching_diff": None,
        "temp_format": None,
        "heating_state": None,
        "lock_state": None,
        "frost_mode": 0x64,
        "enabled": 0x02,
        "frost_temp": 0x07,
        "frost_enable": None,
        "output_delay": None,
        "floor_temp": None,
        "pre_heat": None,
        "floor_state": None
    }

    def __init__(self, network, frame: HeatmiserFrame = None):
        self.__dict__["_params"] = {}
        self._id = None
        self._on_param_change = HeatmiserDevice.on_param_change
        self._net = network
        for param in self.MONITOR_PARAMS.keys():
            self._params[param] = None
        if frame:
            self._declare(frame)

    """Perform initial setup of the device from a discover frame (0x4d)
    """
    def _declare(self, frame: HeatmiserFrame):
        if not frame.is_valid:
            log('warn', "invalid frame:", frame)
            return
        log('debug1', 'device with id', frame.device_id, 'loading from frame:', frame)
        self._id = frame.device_id
        command = frame.command_code

        if command == 0x4d:
            device_type = frame.get_int(2)
            if device_type == HeatmiserDevicePRT.MODEL_CODE:
                if not isinstance(self, HeatmiserDevicePRT):
                    self.__class__ = HeatmiserDevicePRT
                    self.__init__(self._net, frame)
            elif device_type == HeatmiserDevicePRTHW.MODEL_CODE:
                if not isinstance(self, HeatmiserDevicePRTHW):
                    self.__class__ = HeatmiserDevicePRTHW
                    self.__init__(self._net, frame)
        else:
            log('error', "expected command code 0x4d. Got", command, '-', frame)

    """Update the device with current data
    """
    async def handle_frame(self, frame: HeatmiserFrame):
        log('debug', 'Device', self.id, 'got frame:', frame)
        if not frame.is_valid or frame.device_id != self.id:
            log('error', "Invalid frame for device_id", self.id, ":", frame)
        if frame.command_code == self.C_READ_PARAM:
            if len(frame) == 4:
                await self._net.write_frame(frame)
            else:
                self._read_all_from_frame(frame)
        else:
            #param = self._get_param_for_code(frame.command_code)
            #if param and len(frame) == 4:
            #    await self._net.write_frame(frame)
            #else:
            #    log('debug', "Unhandled frame:", frame)
            await self.refresh()

    async def refresh(self):
        log('debug1', f'Device, id {self.id} refreshing')
        frame = HeatmiserFrame(self.id, self.C_READ_PARAM, 0x00)
        await self._net.write_frame(frame)
        
    def _relative_date(self, reference, weekday, hour, minute):
        if reference.weekday() < weekday:
            weekday -= 7
        days = reference.weekday() - weekday
        return (reference - timedelta(days=days)).replace(
            hour=int(hour), minute=int(minute), second=0, microsecond=0)

    async def _send_param_update(self, name, value):
        log('debug', f'sending update to param {name}: {value}')
        if name in self.MONITOR_PARAMS:
            command_code = self.MONITOR_PARAMS[name]
            if command_code == None:
                self._params[name], value = value, self._params[name]
                frame = self._write_all_to_frame()
                self._params[name], value = value, self._params[name]
            else:
                frame = HeatmiserFrame(self.id, command_code + 128, value)
            log('debug', f'Will send frame: {frame}')
            await self._net.write_frame(frame)

    def _get_param_for_code(self, code):
        keys = [k for k, v in self.MONITOR_PARAMS.items() if v == code]
        if keys:
            return keys[0]
        return None
        
    def _read_all_from_frame(self, frame):
        pass

    def _write_all_to_frame(self):
        pass

    @property
    def id(self) -> int:
        return self._id

    def __getattr__(self, name):
        def get_param():
            try:
                return self._params[name]
            except KeyError as e:
                raise AttributeError from e
        return get_param()

    def __setattr__(self, name, value):
        if name.startswith("_") and name[1:] in self._params:
            name = name[1:]
            if self._params[name] != value:
                self._params[name] = value
                if callable(self.on_param_change):
                    self.on_param_change(name, value)
        elif name in self._params:
            asyncio.create_task(self._send_param_update(name, value))
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return (f'ID: {self.id}, Type: {self.TYPE_STR}, '
                f'Room Temp: {self.room_temp}, State: {self.enabled}')

    @property
    def on_param_change(self):
        return self._on_param_change

    @on_param_change.setter
    def on_param_change(self, func):
        self._on_param_change = func


class HeatmiserDevicePRT(HeatmiserDevice):
    MODEL_CODE = 0x51
    C_READ_PARAM = 0x26
    C_WRITE_PARAM = 0xA6
    TYPE_STR = "PRT"

    def __init__(self, network, frame: HeatmiserFrame = None):
        super().__init__(network, frame)
        self._params["sensor_selection"] = None,
        self._params["floor_limit"] = None
        
    def _read_all_from_frame(self, frame):
        now = datetime.now()
        self._pre_heat = frame.get_bits(3, 4, 3)
        self._floor_state = frame.get_bool(3, 7)
        weekday = frame.get_bits(3, 0, 4) - 1
        hour, minute, self._room_temp = frame.get_bytes(4, 3)
        self._datetime = self._relative_date(now, weekday, hour, minute)
        self._part_number = frame.get_bits(7, 0, 4)
        self._switching_diff = frame.get_bits(7, 4, 4)
        self._temp_format, self._frost_enable = frame.get_bool(8, 0, 2)
        self._sensor_selection, self._floor_limit, self._heating_state, \
            self._frost_mode, self._lock_state, self._enabled \
            = frame.get_bool(8, 2, 6)
        self._set_temp, self._frost_temp, self._output_delay, \
            self._floor_temp = frame.get_bytes(9, 4)

    def _write_all_to_frame(self):
        now = datetime.now()
        frame = HeatmiserFrame(self.id, self.C_WRITE_PARAM)
        frame.set_bytes(2, self.MODEL_CODE)
        frame.set_bytes(3, now.weekday() + 1)
        frame.set_bytes(4, now.hour)
        frame.set_bytes(5, now.minute)
        frame.set_bytes(6, self.room_temp)
        frame.set_bytes(7, self.part_number)
        frame.set_bytes(8, self.switching_diff)
        status_bits = [
            self.temp_format, self.frost_enable, self.sensor_selection, self.floor_limit, \
            self.heating_state, self.frost_mode, self.lock_state, self.enabled \
        ]
        status_byte = sum(v<<i for i, v in enumerate(status_bits))
        frame.set_bytes(9, status_byte)
        frame.set_bytes(10, self.set_temp)
        frame.set_bytes(11, self.frost_temp)
        frame.set_bytes(12, self.output_delay)
        frame.set_bytes(13, self.pre_heat)
        frame.set_bytes(14, self.floor_temp)
        #log('debug', "Will write full data:", frame)
        return frame


class HeatmiserDevicePRTHW(HeatmiserDevice):
    MODEL_CODE = 0x52
    C_READ_PARAM = 0x29
    C_WRITE_PARAM = 0xA9
    TYPE_STR = "PRTHW"

    def __init__(self, network, frame: HeatmiserFrame = None):
        super().__init__(network, frame)
        self._params["manual_hw_state"] = None
        self._params["hw_state"] = None

    def _read_all_from_frame(self, frame):
        now = datetime.now()
        weekday = frame.get_bits(3, 0, 4) - 1
        hour, minute, self._room_temp, self._set_temp = frame.get_bytes(4, 4)
        self._datetime = self._relative_date(now, weekday, hour, minute)
        # self._part_number = frame.get_bits(9, 0, 4)
        self._switching_diff = frame.get_int(9)
        self._temp_format, self._frost_enable = frame.get_bool(8, 0, 2)
        self._manual_hw_state, self._hw_state, self._heating_state, \
            self._frost_mode, self._lock_state, self._enabled \
            = frame.get_bool(8, 2, 6)
        self._frost_temp, self._output_delay, self._pre_heat = frame.get_bytes(10, 3)

    def _write_all_to_frame(self):
        now = datetime.now()
        frame = HeatmiserFrame(self.id, self.C_WRITE_PARAM)
        frame.set_bytes(2, self.MODEL_CODE)
        frame.set_bytes(3, now.weekday() + 1)
        frame.set_bytes(4, now.hour)
        frame.set_bytes(5, now.minute)
        frame.set_bytes(6, self.room_temp)
        frame.set_bytes(7, self.set_temp)
        status_bits = [
            self.temp_format, self.frost_enable, self.manual_hw_state, False, \
            False, self.frost_mode, self.lock_state, self.enabled \
        ]
        status_byte = sum(v<<i for i, v in enumerate(status_bits))
        frame.set_bytes(8, status_byte)
        frame.set_bytes(9, self.switching_diff)
        frame.set_bytes(10, self.frost_temp)
        frame.set_bytes(11, self.output_delay)
        frame.set_bytes(12, self.pre_heat)
        frame.set_bytes(13, 0)
        frame.set_bytes(14, 0)
        #log('debug', "Will write full data:", frame)
        return frame
