#!/usr/bin/env python3.9

import asyncio
from heatmiser.network import HeatmiserNetwork
from heatmiser.device import HeatmiserDevice
from heatmiser.logging import log
import heatmiser.logging

heatmiser.logging.LOG_LEVEL = 0

def hm_device_updated(device, param_name, value):
    log('info', f"HM Device Updated - ID: {device.id}, {param_name} = {value}")


async def main():
    HeatmiserDevice.on_param_change = hm_device_updated
    hmn = HeatmiserNetwork('socket://192.168.100.243:1024', range(1, 11))
    await asyncio.gather(hmn.run())
    

if __name__ == "__main__":
    asyncio.run(main())
    print("Done")


"""
data received 01:26:51:02:14:27:14:13:92:15:0c:01:ef:14:2d:c0
data received 02:29:52:01:15:30:13:14:92:02:07:00:03:3b:00:c3
data received 03:26:51:02:14:27:14:13:82:14:11:01:ef:14:2d:b6
data received 04:26:51:02:14:27:10:13:02:15:0c:01:ef:14:2d:2f
data received 05:26:51:02:14:27:14:13:82:0f:0c:01:ef:14:2d:ae
data received 06:26:51:02:14:27:16:23:82:13:0c:01:ef:14:2d:c5
data received 07:26:51:02:14:27:17:23:e2:15:0c:0a:ef:14:2d:32
data received 08:26:51:02:14:27:15:13:82:15:0c:01:ef:14:2d:b8
data received 09:26:51:02:14:27:15:13:c0:15:07:06:ef:14:2d:f7
"""