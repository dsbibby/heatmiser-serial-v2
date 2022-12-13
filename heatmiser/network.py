import asyncio
import serial_asyncio
from heatmiser.protocol import HeatmiserFrame,HeatmiserProtocol
from heatmiser import device
from heatmiser.logging import log


class HeatmiserNetwork:
    def __init__(self, serial_device: str, discovery_range: list):
        self.serial_device = serial_device
        self.queue = asyncio.Queue() # used to handle recieved messages
        self.devices = {}
        self.transport = None
        self.discovery_range = discovery_range
        self.protocol = None
    

    """Build a serial protocol object with queue
    """
    def _protocol_factory(self):
        return HeatmiserProtocol(self.queue)


    """Main run loop
    """
    async def run(self):
        # Create the serial connection 
        loop = asyncio.get_event_loop()
        coro = serial_asyncio.create_serial_connection(loop, self._protocol_factory, self.serial_device, baudrate=4800)
        _, self.protocol = await coro
        # Wait for the serial connection to establish
        while self.protocol.transport is None:
            await asyncio.sleep(1)
        # Start monitoring for incoming frames
        frame_handler = asyncio.create_task(self._handle_frames())
        # Begin device discovery
        log('info', 'Discovering devices...')
        await self._discover_devices(self.discovery_range)
        # Run monitor loop
        log('info', f'Monitoring {len(self.devices.keys())} devices')
        tasks = set()
        tasks.add(asyncio.create_task(self._monitor_loop()))
        tasks.add(frame_handler)
        while self.protocol.transport.serial:
            await asyncio.sleep(5)
        #log('warn', 'cancelling serial handlers')
        #for task in tasks:
        #    task.cancel()


    """Close the serial connection cleanly
    """
    def close(self):
        if self.protocol.transport:
             self.protocol.transport.close()

        
    async def _handle_frames(self):
        while True:
            frame = await self.queue.get()
            log('debug1', 'valid frame:', frame)
            device_id = frame.device_id
            try:
                self.devices[device_id].handle_frame(frame)
            except KeyError:
                new_device = device.HeatmiserDevice(frame=frame)
                if type(new_device) != device.HeatmiserDevice:
                    self.devices[device_id] = new_device
                    log('info', 'Discovered device', new_device)
                

    async def _discover_devices(self, discovery_range):
        for id in discovery_range:
            frame = HeatmiserFrame(id, 0x4d, 0x00)
            await self.protocol.write_frame(frame)
            await asyncio.sleep(.1)
        

    async def _monitor_loop(self):
        while True:
            for id, device in self.devices.items():
                frame = HeatmiserFrame(id, device.C_READ_PARAM, 0x00)
                await self.protocol.write_frame(frame)
                await asyncio.sleep(.1)
