from __future__ import print_function

import os
import sys

import serial

# pylint: disable=unspecified-encoding,consider-using-with
DEVNULL = open(os.devnull, "w")


def list_serial_ports():
    # from https://github.com/pyserial/pyserial/blob/master/serial/tools/list_ports.py
    from serial.tools.list_ports import comports

    result = []
    for port, desc, info in comports():
        if not port or "VID:PID" not in info:
            continue
        split_desc = desc.split(" - ")
        if len(split_desc) == 2 and split_desc[0] == split_desc[1]:
            desc = split_desc[0]
        result.append((port, desc))
    result.sort()
    return result

