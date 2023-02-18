**0PRT-N Heatmiser Protocol**

_Document version: UKHA-PRT-N-0.2_

_Last modified 19/12/2022 14:37_

Contributors: Simon Ryley

Iain Goodhew

**Please note:** This is NOT an official heatmiser document. The information contained within has been obtained by observation and experimentation with a PRT-N Heatmiser thermostat and is in no way guaranteed to be correct. Use of the information below is at the users own risk.

Note there is a new Digital thermostat now from Heatmiser which may not comply with the commands listed in this document.

**Document conventions:**

Numbers highlight in red indicates unknown/ yet to be discovered meaning.

Text/ numbers in yellow are probably correct, but require verification.

All other information is believed to be correct.

**Communications RS-485 single pair 4800,n,8,1**

**Basic message structure:**

A message consists of 4 parts, Address, Command, Data, Checksum.

Address = communications number of stat on the Heatmiser network

Command = single byte command – see below

Data = one or more bytes containing the data for the command, zero if request for data

Checksum = byte addition of Address, Command and Data parts of the message

Lists of commands

| Command | Description | Status\* |
| --- | --- | --- |
| 0x02 | Get thermostat power status | Verified |
| 0x04 | Get temperature set point | Verified |
| 0x07 | Get frost protection temperature | Verified |
| 0x08 | Get room temperature | Verified |
| 0x1a | Get Key lock status | Verified |
| 0x4d | Get Status | Verified |
| 0x4e | Get temperatures and times Mon-Fri | Verified |
| 0x4f | Get temperatures and times Sat-Sun | Verified |
| 0x50 | Get HW Timings Mon-Fri | Verified |
| 0x51 | Get HW Timings Sat-Sun | Verified |
| 0x64 | Get Frost mode | Verified |
|
 |
 |
 |
| 0x82 | Set thermostat power (on/off) | Verified |
| 0x84 | Set Temperature set point | Verified |
| 0x87 | Set frost protection temperature | Verified |
| 0x9a | Set Key lock status | Verified |
| 0xce | Set temperatures and times Mon-Fri | Verified |
| 0xcf | Set temperatures and times Sat-Sun | Verified |
| 0xd0 | Set HW Timings Mon-Fri | Verified |
| 0xd1 | Set HW Timings Sat-Sun | Verified |
| 0xe4 | Set Frost Mode | Verified |
|
 |
 |
 |
|
 |
 |
 |
|
 |
 |
 |

\*

**Detailed Description of commands and replies**

Command 0x02 - Get Thermostat Power Status

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x02 | 0x00 | 0x03 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x02 | 0xff = On ( 0x00 = off) | 0x02 |

Command 0x04 - Get Temperature Set Point

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x04 | 0x00 | 0x05 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x04 | 0x14Set Point Temperature is 20 C | 0x19 |

Command 0x07 – Get frost protection temperature

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x08 | 0x00 | 0x09 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x08 | 0x0cFrost protection temp in degrees C | 0x1d |

Command 0x08 - Get Room Temperature

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x08 | 0x00 | 0x09 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x08 | Current Room TemperatureEg 0x14Temperature is 20 C | 0x1d |

Command 0x1a - Get key lock status

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x1a | 0x00 | 0x1b |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x1a | 0x00 (00= unlocked ff=Locked) | 0x1b |

Command 0x4d – Get Status

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x4d | 0x00 | 0x4e |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 - 6 | 7 |
| Hex Value | 0x01 | 0x4d | 0x51 = (Stat Type PRT-N 0x52 = PRT/HW-N 0x63 = (RoomTemp+0x50) 0x62 = (SetPoint+0x50) 0x50 = NoCall for heat (0x54=call for heat) (0x80=call for hw) (0x84=call for both)


 | 0xb4 |

Command 0x4e – Get temperatures and times Mon-Fri

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x4e | 0x00 | 0x4f |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 - 15 | 16 |
| Hex Value | 0x01 | 0x4e | 0x51 = (Stat Type PRT-N 0x52 = PRT/HW-N) 0x57 =(P1 Hours+0x50) 7 0x50 =(P1 Mins+0x50) 00 0x64 = (P1 Temp+0x50) 20 0x59 = (P2 Hours+0x50) 9 0x50 = (P2 Mins+0x50) 00 0x5f = (P2 Temp+0x50) 15 0x61 = (P3 Hours+0x50) 17 0x50 = (P3 Mins+0x50) 00 0x65 = (P3 Temp+0x50) 21 0x67 = (P4 Hours+0x50) 23 0x50 = (P4 Mins+0x50) 00 0x60 = (P4 Temp+0x50)16
 | 0xE0 |

-- note 0xfa in the hours of a program indicates program not used

Command 0x4f – Get temperatures and times Sat-Sun

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x4f | 0x00 | 0x50 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 - 15 | 16 |
| Hex Value | 0x01 | 0x4f | 0x51 = (Stat Type PRT-N 0x52 = PRT/HW-N) 0x58 =(P1 Hours+0x50) 080x50 =(P1 Mins+0x50) 000x64 = (P1 Temp+0x50) 200x66 = (P2 Hours+0x50) 220x6e = (P2 Mins+0x50) 300x5f = (P2 Temp+0x50) 150xfa = (P3 Hours+0x50) --0x50 = (P3 Mins+0x50) 000x69 = (P3 Temp+0x50) 250xfa = (P4 Hours+0x50) --0x50 = (P4 Mins+0x50) 000x69 = (P4 Temp+0x50)25 | 0x46 |

--note 0xfa in the hours of a program indicates program not used

Command 0x50 – Get HW On off times Mon-Fri

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x50 | 0x52 | 0xnn |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 - 19 | 20 |
| Hex Value | 0x01 | 0x50 | 0x52 = (Stat PRT/HW N) 0x57 =(P1 Hours+0x50) 7 0x50 =(P1 Mins+0x50) 00 0x59 = (P2 Hours+0x50) 9 0x50 = (P2 Mins+0x50) 00 0x61 = (P3 Hours+0x50) 17 0x50 = (P3 Mins+0x50) 00 0x67 = (P4 Hours+0x50) 23 0x50 = (P4 Mins+0x50) 00 0x67 = (P5 Hours+0x50) 0x50 = (P5 Mins+0x50) 0x67 = (P6 Hours+0x50) 0x50 = (P6 Mins+0x50) 0x67 = (P7 Hours+0x50) 0x50 = (P7 Mins+0x50) 0x67 = (P8 Hours+0x50) 0x50 = (P8 Mins+0x50)
 | 0xnn |

-- note 0xfa in the hours of a program indicates program not used

Command 0x51 – Get HW On off times Sat-Sun

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x51 | 0x52 | 0xnn |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 - 19 | 20 |
| Hex Value | 0x01 | 0x51 | 0x52 = (Stat PRT/HW N) 0x57 =(P1 Hours+0x50) 7 0x50 =(P1 Mins+0x50) 00 0x59 = (P2 Hours+0x50) 9 0x50 = (P2 Mins+0x50) 00 0x61 = (P3 Hours+0x50) 17 0x50 = (P3 Mins+0x50) 00 0x67 = (P4 Hours+0x50) 23 0x50 = (P4 Mins+0x50) 00 0x67 = (P5 Hours+0x50) 0x50 = (P5 Mins+0x50) 0x67 = (P6 Hours+0x50) 0x50 = (P6 Mins+0x50) 0x67 = (P7 Hours+0x50) 0x50 = (P7 Mins+0x50) 0x67 = (P8 Hours+0x50) 0x50 = (P8 Mins+0x50)
 | 0xnn |

--note 0xfa in the hours of a program indicates program not used

Command 0x64 – Get Frost mode

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x64 | 0x00 | 0x65 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x64 | 0x00 (00= normal ff=Frost prot) | 0x65 |

Command 0x82 - Set Thermostat Power (on/off)

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x82 | 0xff ( 0xff = On 0x00 = off)
 | 0x82 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x82 | 0xff = On ( 0x00 = off) | 0x82 |

Command 0x84 - Set Temperature Set Point

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x84 | Byte value of temperature in degrees CEg 0x19Set 'Set Point' to 25 C | 0x9e |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x04 | Current Set point TemperatureEg 0x19Set Point is 25 C | 0x1e |

Command 0x87 – Set frost protection temperature

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x88 | 0x0cSet frost protection temp to 12C | 0x9d |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x08 | 0x0cFrost protection temp in degrees C | 0x1d |

Command 0x9a - Set key lock status

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x9a | 0x00(00= unlocked ff=locked) | 0x9b |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0x1a | 0x00 (00= unlocked ff=locked \*) | 0x1b |

\*Note: Key lock must be enabled on the stat. To do this:

- first power off the stat.
- Press A & up for 10 seconds
- 00 = disable, 01 = enable
- Press power off

Command 0xce – Set temperatures and times Mon-Fri

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 - 15 | 16 |
| Hex Value | 0x01 | 0xce | 0x51 = (Stat Type PRT-N 0x52 = PRT/HW-N)0x57 =(P1 Hours+0x50) 70x50 =(P1 Mins+0x50) 000x64 = (P1 Temp+0x50) 200x59 = (P2 Hours+0x50) 90x50 = (P2 Mins+0x50) 000x5f = (P2 Temp+0x50) 150x61 = (P3 Hours+0x50) 170x50 = (P3 Mins+0x50) 000x65 = (P3 Temp+0x50) 210x67 = (P4 Hours+0x50) 230x50 = (P4 Mins+0x50) 000x60 = (P4 Temp+0x50)16
 | 0x60 |

-- note 0xfa in the hours of a program indicates program not used

Reply

None from this command

Command 0xce – Set temperatures and times Sat-Sun

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 - 15 | 16 |
| Hex Value | 0x01 | 0xcf | 0x51 = (Stat Type PRT-N 0x52 = PRT/HW-N)0x57 =(P1 Hours+0x50) 70x50 =(P1 Mins+0x50) 000x64 = (P1 Temp+0x50) 200x59 = (P2 Hours+0x50) 90x50 = (P2 Mins+0x50) 000x5f = (P2 Temp+0x50) 150x61 = (P3 Hours+0x50) 170x50 = (P3 Mins+0x50) 000x65 = (P3 Temp+0x50) 210x67 = (P4 Hours+0x50) 230x50 = (P4 Mins+0x50) 000x60 = (P4 Temp+0x50)16
 | 0x61 |

-- note 0xfa in the hours of a program indicates program not used

Reply

None from this command

Command 0xD0 – Set HW times times Mon-Fri

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 – 19 | 20 |
| Hex Value | 0x01 | 0xd0 | 0x52 = (Stat PRT/HW N) 0x57 =(P1 Hours+0x50) 7 0x50 =(P1 Mins+0x50) 00 0x59 = (P2 Hours+0x50) 9 0x50 = (P2 Mins+0x50) 00 0x61 = (P3 Hours+0x50) 17 0x50 = (P3 Mins+0x50) 00 0x67 = (P4 Hours+0x50) 23 0x50 = (P4 Mins+0x50) 00 0x67 = (P5 Hours+0x50) 0x50 = (P5 Mins+0x50) 0x67 = (P6 Hours+0x50) 0x50 = (P6 Mins+0x50) 0x67 = (P7 Hours+0x50) 0x50 = (P7 Mins+0x50) 0x67 = (P8 Hours+0x50) 0x50 = (P8 Mins+0x50) | 0xnn |

-- note 0xfa in the hours of a program indicates program not used

Reply- None from this command

Command 0xD1 – Set HW times times Sat\Sun

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 – 19 | 20 |
| Hex Value | 0x01 | 0xd1 | 0x52 = (Stat PRT/HW N) 0x57 =(P1 Hours+0x50) 7 0x50 =(P1 Mins+0x50) 00 0x59 = (P2 Hours+0x50) 9 0x50 = (P2 Mins+0x50) 00 0x61 = (P3 Hours+0x50) 17 0x50 = (P3 Mins+0x50) 00 0x67 = (P4 Hours+0x50) 23 0x50 = (P4 Mins+0x50) 00 0x67 = (P5 Hours+0x50) 0x50 = (P5 Mins+0x50) 0x67 = (P6 Hours+0x50) 0x50 = (P6 Mins+0x50) 0x67 = (P7 Hours+0x50) 0x50 = (P7 Mins+0x50) 0x67 = (P8 Hours+0x50) 0x50 = (P8 Mins+0x50) | 0xnn |

-- note 0xfa in the hours of a program indicates program not used

Reply- None from this command

Command 0xe4 – Set Frost mode

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0xe4 | 0x00 | 0xe5 |

Reply

| Description | Address | Command | Data | Checksum |
| --- | --- | --- | --- | --- |
| Byte Position | 1 | 2 | 3 | 4 |
| Hex Value | 0x01 | 0xe4 | 0x00 (00= normal ff=Frost Prot) | 0xe5 |