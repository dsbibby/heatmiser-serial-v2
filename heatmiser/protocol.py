import asyncio
from datetime import datetime, timedelta
from heatmiser.logging import log
from heatmiser.frame import HeatmiserFrame


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
        log('debug1', 'protocol received frame:', frame)
        asyncio.ensure_future(self.queue.put(frame))
        self._lastwrite = None

    def connection_lost(self, exc):
        log('debug', 'port closed')
        # self.transport.loop.stop()

    def pause_writing(self):
        log('debug', 'pause writing')
        log('debug', self.transport.get_write_buffer_size())

    def resume_writing(self):
        log('debug', self.transport.get_write_buffer_size())
        log('debug', 'resume writing')

    async def write_frame(self, frame):
        if self._lastwrite:
            start = datetime.now()
            log('debug1', 'protocol write delayed awaiting previous rx')
            while self._lastwrite and \
                    self._lastwrite + timedelta(seconds=2) > datetime.now():
                await asyncio.sleep(0.2)
            log('debug1', 'protocol waited', (datetime.now() - start).seconds,
                'seconds before writing')
        log('debug1', "protocol writing frame:", frame)
        self.transport.write(frame.data)
        self._lastwrite = datetime.now()
