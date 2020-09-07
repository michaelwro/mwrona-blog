---
title: "Read Serial Data From Spektrum Remote Receiver"
date: "2020-09-02"
author: Michael Wrona
draft: false
tags: ["arduino", "circuits", "cpp", "drone"]
---

About six years ago, I purchased a [Spektrum DX6i](https://www.spektrumrc.com/Products/Default.aspx?ProdId=SPM6630) RC plane transmitter to fly my RC planes with. Unfortunately, life got busier and my interests shifted, which sent my planes and controller to retire in the basement. When the idea to build a quadcopter flight controller began to come to fruition, I knew my DX6i controller would be perfect! "This is a cause worth coming out of retirement for, old one" I said to my controller. His response: not powering on. I guess it's time for some fresh AA's.

## Introduction

I was initially going to use my [Spektrum AR6210 6-channel receiver](https://www.spektrumrc.com/Products/Default.aspx?ProdId=SPMAR6210) to provide pilot inputs to my quadcopter. I'd use my microcontroller's digital pins to read the [PWM signals](https://en.wikipedia.org/wiki/Pulse-width_modulation) from each channel. Unfortuantely, reading six PWM channels would require six individual servo cables running from the receiver to the microcontroller, which would look messy and add extra weight to the drone. Since this was basically my only option given the materials I had, I was willing to compromise.

I had always wondered what the little dongle-thingy was attached to my AR6210 receiver. I did some research and discovered this was a [Spektrum DSMX Remote Receiver](https://www.spektrumrc.com/Products/Default.aspx?ProdID=SPM9645). I did some more digging and found out that the three wires connecting the Remote Receiver to the AR6210 were power (+3.3V, orange), data (gray), and ground (black) wires. It turns out that the connection between the two was a serial connection that contained channel data! After this amazing discovery, I began reverse engineering the DSMX communication protocol and eventually succeeded: I figured out how to extract the six channel/transmitter stick positions from the DSMX serial byte stream. Now, time to tell you how to do the same!

{{< figure src="/post-imgs/03-read-spektrum-sat-data/rem-rec-and-rc-rec.jpg" alt="Remote Receiver and RC Receiver"
width="400px" position="center" style="border-radius: 8px;"
caption="Spektrum Remote Receiver and AR6210 RC Receiver." captionPosition="center">}}

First, I'll describe the DSMX communication protocol and serial packet structure. Next, I'll outline my hardware testing setup and wiring. Finally, I'll dive deep into the Arduino code I developed to read and process the remote receiver's serial data stream.

## DSMX Communication Protocol

**Datasheet Reference:** The official data sheet describing the Spektrum Remote Receiver communication protol can be found [at this link](https://www.spektrumrc.com/ProdInfo/Files/Remote%20Receiver%20Interfacing%20Rev%20A.pdf).

The serial communication protocol used by Spektrum Remote Receivers consists of 16-byte transmission packets. There are four different serial communication protocols used by the receivers, differentiated by the timing between transmissions and channel data ranges.

| Protocol | ID Byte | TX Timing | Ch. Data Range |
| :---     | :---:   | :---:     | :---:          |
| **11ms/2048 DSM2** | 0x12 | 11ms | 0 ... 2048 |
| **22ms/1024 DSM2** | 0x01 | 22ms | 0 ... 1024 |
| **11ms/2048 DSMX** | 0xB2 | 11ms | 0 ... 2048 |
| **22ms/2048 DSMX*** | 0xA2 | 22ms | 0 ... 2048 |

The timing between each serial data packet transmission is either 11ms or 22ms, and the channel data ranges from zero to either 1024 or 2048. **My particular Remote Receiver used the 22ms/2048 DSMX (denoted by \*) protocol.** I am assuming this is the most common.

### Packet Structure

Each 16-byte serial data packet has the following structure:

{{<rawhtml>}}
<table>
    <tr>
        <th>Byte Index</th>
        <td>0</td>
        <td>1</td>
        <td>2 ... 15</td>
    </tr>
    <tr>
        <th>Field Name</th>
        <td>Fades</td>
        <td>Proto. ID</td>
        <td>ServoData[7]</td>
    </tr>
    <tr>
        <th>Data Type</th>
        <td>uint8_t</td>
        <td>uint8_t</td>
        <td>uint16_t</td>
    </tr>
</table>
{{</rawhtml>}}

The first byte in the transmission is referred to as 'fades' in Spektrum's datasheet. This is a count of how many data packets were missed by the remote receiver. My receiver never missed any frames during testing (even when I did a range test), so I guess there's no need to keep track of this value in your code. This byte is an unsigned 8-bit value. The second byte is the protocol ID byte. This important byte's value indicates which protocol the remote receiver uses. This byte is an unsigned 8-bit value. Finally, the remaining 14 bytes in the serial packet describe the seven channel's values/positions. These are [big-endian](https://en.wikipedia.org/wiki/Endianness) unsigned 16-bit values. Therefore, each channel's data is in groups of two 8-bit unsigned values. Each of these groups have the following bit-structure:

{{<rawhtml>}}
<table>
    <tr>
        <th>Bit 15</th>
        <td>Channel phase</td>
    </tr>
    <tr>
        <th>Bits 14 - 11</th>
        <td>Channel ID</td>
    </tr>
    <tr>
        <th>Bits 10 - 0</th>
        <td>Channel Value</td>
    </tr>
</table>
{{</rawhtml>}}

This will begin to make more sense when I describe my data processing code down below.

## Hardware Setup and Wiring

### Custom Plug Adapter

In order to make the remote receiver breadboard-compatible, I needed to make my own custom adapter. I bought a additional [remote receiver cable](https://www.amazon.com/gp/product/B000ND6IXW/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1) and soldered its wires to the wires of a standard servo connector (see image below).

{{< figure src="/post-imgs/03-read-spektrum-sat-data/rec-wire-conv.jpg" alt="Custom wire adaptor."
width="400px" position="center" style="border-radius: 8px;"
caption="Custom adapter to convert the remote receiver connector to a standard servo plug." captionPosition="center">}}

When it came time to 




In order to determine which protocol my remote receiver used, I probed its serial output via a serial-to-USB converter and serial port monitoring software.




<!-- 
Anyways, when I began brainstorming ways to provide pilot inputs to my quadcopter, I came up with two methods:

1. Read the RC receiver's PWM servo outputs, or
2. Read Spektrum Remote Receiver's data



### RC Receiver PWM Signals

The first option was to read the [PWM](https://en.wikipedia.org/wiki/Pulse-width_modulation) servo outputs from my [Spektrum AR6210 6-channel receiver](https://www.spektrumrc.com/Products/Default.aspx?ProdId=SPMAR6210). This is pretty easy and straightforward to accomplish with Arduino microcontrollers. An Arduino's digital pins can measure the duration between pulse rises and falls and compute pulse widths in units of microseconds (us). There are a couple of drawbacks to this method. First and foremost, this method would require six servo cables running from the receiver to the microcontroller, which would look very messy and add extra weight to the quadcopter. Second, simultaneously reading six PWM signals would take precious CPU clock cycles away from computing more important things, such as sensor fusion and flight control algorithms - the very things keeping the drone in the air!

{{< figure src="/post-imgs/03-read-spektrum-sat-data/rem-rec-and-rc-rec.jpg" alt="Remote Receiver and RC Receiver"
width="400px" position="center" style="border-radius: 8px;"
caption="Spektrum Remote Receiver and AR6210 RC Receiver." captionPosition="center">}}

### Spektrum Satellite Receivers

The second option I came up with, and the primary focus of this blog post, was reading the data stream being transmitted by the [Spektrum Remote Receiver](https://www.spektrumrc.com/Products/Default.aspx?ProdID=SPM9645) attached to my AR6210 receiver. The  -->



