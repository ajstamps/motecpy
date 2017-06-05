# MoTeCPy file for WHR17 Dash
# Reads from a CAN bus that is connected to a MoTeC ECU
# Created by Alex Stamps
# 4-29-17

import os
from can import *
import crcmod


class MoTeCPy:
    def __init__(self, can_init='vcan0'):
        self.can_init = can_init

        if self.can_init == 'vcan0':  # CAN Bus gets initialized here.
            os.system("sudo modprobe vcan")
            os.system("sudo ip link add dev vcan0 type vcan")
            os.system("sudo ip link set up vcan0")
            print("started vcan")
        else:
            os.system("sudo /sbin/ip link set can0 up type can bitrate 1000000")
            print("started can")

        try:  # try to initialize the CAN for use.
            self.bus = interface.Bus(channel=self.can_init, bustype='socketcan_native')
            print("BUS and reader initialized initialized")
        except OSError:  # if this error pops up, it didn't work. Maybe try restarting the Pi and/or program
            print('Cannot find PiCAN board.')
            exit()

        self.can_data = [Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message,
                         Message]

        self.temp_data = [Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message]

        self.prev_data = [Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message,
                          Message]

        self.crc32_func = crcmod.predefined.mkCrcFun('crc-32')

    def __del__(self):
        print("\nCleaning Up\n")

    def get_data(self):
        i = 0
        if self.crc_check():
            self.prev_data = self.can_data[:]
        msg = self.bus.recv()
        self.temp_data[i] = msg

        while not self.is_message_start():
            msg = self.bus.recv()
            self.temp_data[i] = msg

        while i < 21:
            i += 1
            msg = self.bus.recv()
            self.temp_data[i] = msg

        if self.crc_check():
            self.can_data = self.temp_data[:]

    def get(self, val):
        try:
            return {
                'rpm': self.can_data[0].data[4] * 256 + self.can_data[0].data[5],

                'tps': (self.can_data[0].data[6] * 256 + self.can_data[0].data[7]) * 0.1,

                'manifold pressure': (self.can_data[1].data[0] * 256 + self.can_data[1].data[1]) * 0.1,

                'air temp': (self.can_data[1].data[2] * 256 + self.can_data[1].data[3]) * 0.1,

                'engine temp': (self.can_data[1].data[4] * 256 + self.can_data[1].data[5]) * 0.1,

                'lambda1': (self.can_data[1].data[6] * 256 + self.can_data[1].data[7]) * 0.001,

                'lambda2': (self.can_data[2].data[0] * 256 + self.can_data[2].data[1]) * 0.001,

                'exhaust manifold pressure': (self.can_data[2].data[2] * 256 + self.can_data[2].data[3]) * 0.1,

                'mass air flow': (self.can_data[2].data[4] * 256 + self.can_data[2].data[5]) * 0.1,

                'fuel temp': (self.can_data[2].data[6] * 256 + self.can_data[2].data[7]) * 0.1,

                'fuel pressure': (self.can_data[3].data[0] * 256 + self.can_data[3].data[1]) * 0.1,

                'oil temp': (self.can_data[3].data[2] * 256 + self.can_data[3].data[3]) * 0.1,

                'oil pressure': (self.can_data[3].data[4] * 256 + self.can_data[3].data[5]) * 0.1,

                'gear voltage': (self.can_data[3].data[6] * 256 + self.can_data[3].data[7]) * 0.01,

                'knock voltage': (self.can_data[4].data[0] * 256 + self.can_data[4].data[1]) * 0.1,

                'gear shift force': (self.can_data[4].data[2] * 256 + self.can_data[4].data[3]) * 0.1,

                'exhaust temp1': self.can_data[4].data[4] * 256 + self.can_data[4].data[5],

                'exhaust temp2': self.can_data[4].data[6] * 256 + self.can_data[4].data[7],

                'user channel1': (self.can_data[5].data[0] * 256 + self.can_data[5].data[1]) * 0.1,

                'user channel2': (self.can_data[5].data[2] * 256 + self.can_data[5].data[3]) * 0.1,

                'user channel3': (self.can_data[5].data[4] * 256 + self.can_data[5].data[5]) * 0.1,

                'user channel4': (self.can_data[5].data[6] * 256 + self.can_data[5].data[7]) * 0.1,

                'battery voltage': (self.can_data[6].data[0] * 256 + self.can_data[6].data[1]) * 0.01,

                'ecu temp': (self.can_data[6].data[2] * 256 + self.can_data[6].data[3]) * 0.1,

                'digital input1 speed': (self.can_data[6].data[4] * 256 + self.can_data[6].data[5]) * 0.1,

                'digital input2 speed': (self.can_data[6].data[6] * 256 + self.can_data[6].data[7]) * 0.1,

                'digital input3 speed': (self.can_data[7].data[0] * 256 + self.can_data[7].data[1]) * 0.1,

                'digital input4 speed': (self.can_data[7].data[2] * 256 + self.can_data[7].data[3]) * 0.1,

                'drive speed': (self.can_data[7].data[4] * 256 + self.can_data[7].data[5]) * 0.1,

                'ground speed': (self.can_data[7].data[6] * 256 + self.can_data[7].data[7]) * 0.1,

                'slip': (self.can_data[8].data[0] * 256 + self.can_data[8].data[1]) * 0.1,

                'aim slip': (self.can_data[8].data[2] * 256 + self.can_data[8].data[3]) * 0.1,

                'launch rpm': (self.can_data[8].data[4] * 256 + self.can_data[8].data[5]) * 0.1,

                'gear': self.can_data[14].data[4] * 256 + self.can_data[14].data[5],

                'low battery': self.can_data[16].data[7] & 1,

                'no sync': self.can_data[16].data[7] & 4,

                'sync': self.can_data[16].data[6] & 8,

                'no ref': self.can_data[16].data[6] & 16,

                'ref': self.can_data[16].data[6] & 32,

                'rpm over': self.can_data[16].data[6] & 64
            }[val]
        except (IndexError, AttributeError):  # If the normal get fails, it sends the previous data good data
            return {
                'rpm': self.prev_data[0].data[4] * 256 + self.prev_data[0].data[5],

                'tps': (self.prev_data[0].data[6] * 256 + self.prev_data[0].data[7]) * 0.1,

                'manifold pressure': (self.prev_data[1].data[0] * 256 + self.prev_data[1].data[1]) * 0.1,

                'air temp': (self.prev_data[1].data[2] * 256 + self.prev_data[1].data[3]) * 0.1,

                'engine temp': (self.prev_data[1].data[4] * 256 + self.prev_data[1].data[5]) * 0.1,

                'lambda1': (self.prev_data[1].data[6] * 256 + self.prev_data[1].data[7]) * 0.001,

                'lambda2': (self.prev_data[2].data[0] * 256 + self.prev_data[2].data[1]) * 0.001,

                'exhaust manifold pressure': (self.prev_data[2].data[2] * 256 + self.prev_data[2].data[3]) * 0.1,

                'mass air flow': (self.prev_data[2].data[4] * 256 + self.prev_data[2].data[5]) * 0.1,

                'fuel temp': (self.prev_data[2].data[6] * 256 + self.prev_data[2].data[7]) * 0.1,

                'fuel pressure': (self.prev_data[3].data[0] * 256 + self.prev_data[3].data[1]) * 0.1,

                'oil temp': (self.prev_data[3].data[2] * 256 + self.prev_data[3].data[3]) * 0.1,

                'oil pressure': (self.prev_data[3].data[4] * 256 + self.prev_data[3].data[5]) * 0.1,

                'gear voltage': (self.prev_data[3].data[6] * 256 + self.prev_data[3].data[7]) * 0.01,

                'knock voltage': (self.prev_data[4].data[0] * 256 + self.prev_data[4].data[1]) * 0.1,

                'gear shift force': (self.prev_data[4].data[2] * 256 + self.prev_data[4].data[3]) * 0.1,

                'exhaust temp1': self.prev_data[4].data[4] * 256 + self.prev_data[4].data[5],

                'exhaust temp2': self.prev_data[4].data[6] * 256 + self.prev_data[4].data[7],

                'user channel1': (self.prev_data[5].data[0] * 256 + self.prev_data[5].data[1]) * 0.1,

                'user channel2': (self.prev_data[5].data[2] * 256 + self.prev_data[5].data[3]) * 0.1,

                'user channel3': (self.prev_data[5].data[4] * 256 + self.prev_data[5].data[5]) * 0.1,

                'user channel4': (self.prev_data[5].data[6] * 256 + self.prev_data[5].data[7]) * 0.1,

                'battery voltage': (self.prev_data[6].data[0] * 256 + self.prev_data[6].data[1]) * 0.01,

                'ecu temp': (self.prev_data[6].data[2] * 256 + self.prev_data[6].data[3]) * 0.1,

                'digital input1 speed': (self.prev_data[6].data[4] * 256 + self.prev_data[6].data[5]) * 0.1,

                'digital input2 speed': (self.prev_data[6].data[6] * 256 + self.prev_data[6].data[7]) * 0.1,

                'digital input3 speed': (self.prev_data[7].data[0] * 256 + self.prev_data[7].data[1]) * 0.1,

                'digital input4 speed': (self.prev_data[7].data[2] * 256 + self.prev_data[7].data[3]) * 0.1,

                'drive speed': (self.prev_data[7].data[4] * 256 + self.prev_data[7].data[5]) * 0.1,

                'ground speed': (self.prev_data[7].data[6] * 256 + self.prev_data[7].data[7]) * 0.1,

                'slip': (self.prev_data[8].data[0] * 256 + self.prev_data[8].data[1]) * 0.1,

                'aim slip': (self.prev_data[8].data[2] * 256 + self.prev_data[8].data[3]) * 0.1,

                'launch rpm': (self.prev_data[8].data[4] * 256 + self.prev_data[8].data[5]) * 0.1,

                'gear': self.prev_data[14].data[4] * 256 + self.prev_data[14].data[5],

                'low battery': self.prev_data[16].data[7] & 1,

                'no sync': self.prev_data[16].data[7] & 4,

                'sync': self.prev_data[16].data[6] & 8,

                'no ref': self.prev_data[16].data[6] & 16,

                'ref': self.prev_data[16].data[6] & 32,

                'rpm over': self.prev_data[16].data[6] & 64,

                'error': False
            }[val]

    def is_message_start(self):
        try:
            return self.temp_data[0].data[0] == 130 and self.temp_data[0].data[1] == 129 \
                   and self.temp_data[0].data[2] == 128 and self.temp_data[0].data[3] == 84
        except AttributeError:
            return False

    def crc_check(self):
        try:
            dataval = bytearray()
            check = True

            for i in range(22):
                if i < 21:
                    for j in range(8):
                        dataval.append(self.temp_data[i].data[j])
                else:
                    for j in range(4):
                        dataval.append(self.temp_data[i].data[j])

            crc = hex(self.crc32_func(dataval))
            splitdataval = [crc[i:i + 2] for i in range(0, len(crc), 2)]

            for i in range(4):
                if hex(int(splitdataval[i + 1], 16)) == hex(self.temp_data[21].data[i + 4]) and check:
                    check = True
                else:
                    check = False

        except (IndexError, AttributeError):
            return False

        return check
