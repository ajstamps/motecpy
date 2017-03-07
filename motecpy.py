import os
import can


class MoTeCPy:
    def __init__(self, can_init='can0'):
        self.can_init = can_init
        if self.can_init == 'vcan0':  # CAN Bus gets initialized here. Change
            os.system("sudo modprobe vcan")
            os.system("sudo ip link add dev vcan0 type vcan")
            os.system("sudo ip link set up vcan0")
            print("started vcan")
        else:
            os.system("sudo /sbin/ip link set can0 up type can bitrate 1000000")
            print("started can")

        try:  # try to initialize the CAN for use.
            self.bus = can.interface.Bus(channel=self.can_init, bustype='socketcan_native')
            print("BUS initialized")
        except OSError:  # if this error pops up, it didn't work. Maybe try restarting the Pi
            print('Cannot find PiCAN board.')
            exit()

        print("Waiting for CAN Signal...")
        self.can_data = []
        print("CAN Signal found, beginning transmission")

    def __del__(self):
        if self.can_init == 'vcan0':
            os.system("sudo ip link set vcan0 down")
        else:
            os.system("sudo /sbin/ip link set can0 down")

    def get_data(self):
        self.can_data[0] = self.bus.recv()
        msg = self.bus.recv()
        i = 0

        while not self.is_message_start():
            self.can_data[i] = self.bus.recv()
            i += 1

        while i < 22:
            if self.check_message(msg):
                self.can_data[i] = self.bus.recv()
            i += 1

    def get_rpm(self):
        return self.can_data[0].data[4] * 256 + self.can_data[0].data[5]

    def get_throttle_position(self):
        return (self.can_data[0].data[6] * 256 + self.can_data[0].data[7]) * 0.1

    def get_manifold_pressure(self):
        return (self.can_data[1].data[0] * 256 + self.can_data[1].data[1]) * 0.1

    def get_air_temp(self):
        return (self.can_data[1].data[2] * 256 + self.can_data[1].data[3]) * 0.1

    def get_engine_temp(self):
        return (self.can_data[1].data[4] * 256 + self.can_data[1].data[5]) * 0.1

    def get_lambda1(self):
        return (self.can_data[1].data[6] * 256 + self.can_data[1].data[7]) * 0.001

    def get_lambda2(self):
        return (self.can_data[2].data[0] * 256 + self.can_data[2].data[1]) * 0.001

    def get_exhaust_manifold_pressure(self):
        return (self.can_data[2].data[2] * 256 + self.can_data[2].data[3]) * 0.1

    def get_mass_air_flow(self):
        return (self.can_data[2].data[4] * 256 + self.can_data[2].data[5]) * 0.1

    def get_fuel_temp(self):
        return (self.can_data[2].data[6] * 256 + self.can_data[2].data[7]) * 0.1

    def get_fuel_pressure(self):
        return (self.can_data[3].data[0] * 256 + self.can_data[3].data[1]) * 0.1

    def get_oil_temp(self):
        return (self.can_data[3].data[2] * 256 + self.can_data[3].data[3]) * 0.1

    def get_oil_pressure(self):
        return (self.can_data[3].data[4] * 256 + self.can_data[3].data[5]) * 0.1

    def get_gear_voltage(self):
        return (self.can_data[3].data[6] * 256 + self.can_data[3].data[7]) * 0.01

    def get_knock_voltage(self):
        return (self.can_data[4].data[0] * 256 + self.can_data[4].data[1]) * 0.1

    def get_gear_shift_force(self):
        return (self.can_data[4].data[2] * 256 + self.can_data[4].data[3]) * 0.1

    def get_exhaust_temp1(self):
        return self.can_data[4].data[4] * 256 + self.can_data[4].data[5]

    def get_exhaust_temp2(self):
        return self.can_data[4].data[6] * 256 + self.can_data[4].data[7]

    def get_user_channel1(self):
        return (self.can_data[5].data[0] * 256 + self.can_data[5].data[1]) * 0.1

    def get_user_channel2(self):
        return (self.can_data[5].data[2] * 256 + self.can_data[5].data[3]) * 0.1

    def get_user_channel3(self):
        return (self.can_data[5].data[4] * 256 + self.can_data[5].data[5]) * 0.1

    def get_user_channel4(self):
        return (self.can_data[5].data[6] * 256 + self.can_data[5].data[7]) * 0.1

    def get_battery_voltage(self):
        return (self.can_data[6].data[0] * 256 + self.can_data[6].data[1]) * 0.01

    def get_ecu_temp(self):
        return (self.can_data[6].data[2] * 256 + self.can_data[6].data[3]) * 0.1

    def get_digital_input1_speed(self):
        return (self.can_data[6].data[4] * 256 + self.can_data[6].data[5]) * 0.1

    def get_digital_input2_speed(self):
        return (self.can_data[6].data[6] * 256 + self.can_data[6].data[7]) * 0.1

    def get_digital_input3_speed(self):
        return (self.can_data[7].data[0] * 256 + self.can_data[7].data[1]) * 0.1

    def get_digital_input4_speed(self):
        return (self.can_data[7].data[2] * 256 + self.can_data[7].data[3]) * 0.1

    def get_drive_speed(self):
        return (self.can_data[7].data[4] * 256 + self.can_data[7].data[5]) * 0.1

    def get_ground_speed(self):
        return (self.can_data[7].data[6] * 256 + self.can_data[7].data[7]) * 0.1

    def get_slip(self):
        return (self.can_data[8].data[0] * 256 + self.can_data[8].data[1]) * 0.1

    def get_aim_slip(self):
        return (self.can_data[8].data[2] * 256 + self.can_data[8].data[3]) * 0.1

    def get_launch_rpm(self):
        return (self.can_data[8].data[4] * 256 + self.can_data[8].data[5]) * 0.1

    def get_gear(self):
        return (self.can_data[14].data[4] * 256 + self.can_data[14].data[5]) / 10

    # def get_low_bat_err(self):
    #     return self.can_data[16].data[2] & 128

    def is_message_start(self):
        return self.can_data[0].data[0] == 130 and self.can_data[0].data[1] == 129 \
               and self.can_data[0].data[2] == 128 and self.can_data[0].data[3] == 84

    @staticmethod
    def check_message(msg):
        if msg.arbitration_id is 0x0E8:
            return True
        else:
            return False
