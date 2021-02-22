import asyncio
import serial_asyncio
from heatmiser import protocol
from heatmiser import device

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
        return protocol.HeatmiserProtocol(self.queue)

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
        frame_handler = asyncio.ensure_future(self._handle_frames())
        # Begin device discovery
        print("Discovering devices...")
        await self._discover_devices(self.discovery_range)
        # Run monitor loop
        print(f"Monitoring {len(self.devices.keys())} devices")
        await asyncio.gather(self._monitor_loop(), frame_handler)

    async def _handle_frames(self):
        while True:
            frame = await self.queue.get()
            print('valid frame:', frame)
            device_id = frame.device_id
            try:
                self.devices[device_id].handle_frame(frame)
            except KeyError:
                self.devices[device_id] = device.HeatmiserDevice(frame=frame)
            #for dev in self.devices.values():
            #    print(dev)
                
    async def _discover_devices(self, discovery_range):
        for id in discovery_range:
            frame = protocol.HeatmiserFrame(id, 0x4d, 0x00)
            self.protocol.write_frame(frame)
            await asyncio.sleep(.2)
        
    async def _monitor_loop(self):
        while True:
            for id, device in self.devices.items():
                frame = protocol.HeatmiserFrame(id, device.C_READ_PARAM, 0x00)
                self.protocol.write_frame(frame)
                await asyncio.sleep(.2)
