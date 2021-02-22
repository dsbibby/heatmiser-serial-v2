# heatmiser-serial-v2
An asyncio compatible Python module to allow communication with Heatmiser Serial devices using the v2 protocol.

## Requirements
* Python 3.9
* Heatmiser v2 Stats (to identify v2 stats, breifly press the power button. A v2 stat will switch off. A v3 stat will enter frost protect mode.)
* RS485 to serial (or IP) adapter (I used a [USR-TCP232-24 Module](https://www.google.com/search?q=usr-tcp232-24))
