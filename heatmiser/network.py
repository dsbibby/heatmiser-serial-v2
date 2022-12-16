import asyncio
import serial_asyncio
from heatmiser.protocol import HeatmiserFrame,HeatmiserProtocol
from heatmiser import device
from heatmiser.logging import log


class HeatmiserNetwork:
    def __init__(self, serial_device: str, discovery_range: list):
        self._serial_device = serial_device
        self._queue = asyncio.Queue() # used to handle recieved messages
        self._devices = {}
        self._transport = None
        self._discovery_range = discovery_range
        self._protocol = None
        self._on_device_discovered = None
    

    """Build a serial protocol object with queue
    """
    def _protocol_factory(self):
        return HeatmiserProtocol(self._queue)


    async def run(self):
        """Main run loop
        """
        # Create the serial connection 
        loop = asyncio.get_event_loop()
        coro = serial_asyncio.create_serial_connection(loop, self._protocol_factory, self._serial_device, baudrate=4800)
        _, self._protocol = await coro
        # Wait for the serial connection to establish
        while self._protocol.transport is None:
            await asyncio.sleep(1)
        # Start monitoring for incoming frames
        frame_handler = asyncio.create_task(self._handle_frames())
        # Begin device discovery
        log('info', 'Discovering devices...')
        await self._discover_devices(self._discovery_range)
        # Run monitor loop
        log('info', f'Monitoring {len(self._devices.keys())} devices')
        tasks = set()
        tasks.add(asyncio.create_task(self._monitor_loop()))
        tasks.add(frame_handler)
        while self._protocol.transport.serial:
            await asyncio.sleep(5)
        #log('warn', 'cancelling serial handlers')
        #for task in tasks:
        #    task.cancel()


    """ Close the serial connection cleanly

    """
    def close(self):
        if self._protocol.transport:
            self._protocol.transport.close()


    async def _handle_frames(self):
        while True:
            frame = await self._queue.get()
            log('debug1', 'valid frame:', frame)
            device_id = frame.device_id
            try:
                self._devices[device_id].handle_frame(frame)
            except KeyError:
                new_device = device.HeatmiserDevice(frame=frame)
                if type(new_device) != device.HeatmiserDevice:
                    self._devices[device_id] = new_device
                    log('info', 'Discovered device', new_device)
                    if callable(self.on_device_discovered):
                        self.on_device_discovered(new_device)


    async def _discover_devices(self, discovery_range):
        for _id in discovery_range:
            frame = HeatmiserFrame(_id, 0x4d, 0x00)
            await self._protocol.write_frame(frame)
            await asyncio.sleep(.1)


    async def _monitor_loop(self):
        while True:
            for _id, _device in self._devices.items():
                frame = HeatmiserFrame(_id, _device.C_READ_PARAM, 0x00)
                await self._protocol.write_frame(frame)
                await asyncio.sleep(.1)

    @property
    def on_device_discovered(self):
        return self._on_device_discovered
    
    @on_device_discovered.setter
    def on_device_discovered(self, func):
        self._on_device_discovered = func