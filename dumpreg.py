#!/usr/bin/env python3
import os
import argparse
import minimalmodbus
import serial

dict_registers = {
    #### REALTIME DATA ####
          "DEVICE_OVERTEMPERATURE": [0x2000, 0, 0x02, None, False, None, None],
              "ARRAY_DAY_OR_NIGHT": [0x200C, 0, 0x02, None, False, None, None],
                   "ARRAY_VOLTAGE": [0x3100, 2, 0x04, None, False, 100, "V"],
                   "ARRAY_CURRENT": [0x3101, 2, 0x04, None, False, 100, "A"],
                   "ARRAY_POWER_L": [0x3102, 0, 0x04, None, False, 100, "W"],
                   "ARRAY_POWER_H": [0x3103, 0, 0x04, None, False, 100, "W"],
                    "LOAD_VOLTAGE": [0x310C, 2, 0x04, None, False, 100, "V"],
                    "LOAD_CURRENT": [0x310D, 2, 0x04, None, False, 100, "A"],
                    "LOAD_POWER_L": [0x310E, 0, 0x04, None, False, 100, "W"],
                    "LOAD_POWER_H": [0x310F, 0, 0x04, None, False, 100, "W"],
             "BATTERY_TEMPERATURE": [0x3110, 2, 0x04, None, False, 100, "°C"],
              "DEVICE_TEMPERATURE": [0x3111, 2, 0x04, None, False, 100, "°C"],
                     "BATTERY_SOC": [0x311A, 0, 0x04, None, False, 1, "%"],
                  "BATTERY_STATUS": [0x3200, 0, 0x04, None, False, None, None],
       "CHARGING_EQUIPMENT_STATUS": [0x3201, 0, 0x04, None, False, None, None],
    "DISCHARGING_EQUIPMENT_STATUS": [0x3202, 0, 0x04, None, False, None, None],
           "TODAY_MAX_BAT_VOLTAGE": [0x3302, 2, 0x04, None, False, 100, "V"],
           "TODAY_MIN_BAT_VOLTAGE": [0x3303, 2, 0x04, None, False, 100, "V"],
         "TODAY_CONSUMED_ENERGY_L": [0x3304, 0, 0x04, None, False, 100, "kWh"],
         "TODAY_CONSUMED_ENERGY_H": [0x3305, 0, 0x04, None, False, 100, "kWh"],
         "MONTH_CONSUMED_ENERGY_L": [0x3306, 0, 0x04, None, False, 100, "kWh"],
         "MONTH_CONSUMED_ENERGY_H": [0x3307, 0, 0x04, None, False, 100, "kWh"],
          "YEAR_CONSUMED_ENERGY_L": [0x3308, 0, 0x04, None, False, 100, "kWh"],
          "YEAR_CONSUMED_ENERGY_H": [0x3309, 0, 0x04, None, False, 100, "kWh"],
         "TOTAL_CONSUMED_ENERGY_L": [0x330A, 0, 0x04, None, False, 100, "kWh"],
         "TOTAL_CONSUMED_ENERGY_H": [0x330B, 0, 0x04, None, False, 100, "kWh"],
        "TODAY_GENERATED_ENERGY_L": [0x330C, 0, 0x04, None, False, 100, "kWh"],
        "TODAY_GENERATED_ENERGY_H": [0x330D, 0, 0x04, None, False, 100, "kWh"],
        "MONTH_GENERATED_ENERGY_L": [0x330E, 0, 0x04, None, False, 100, "kWh"],
        "MONTH_GENERATED_ENERGY_H": [0x330F, 0, 0x04, None, False, 100, "kWh"],
         "YEAR_GENERATED_ENERGY_L": [0x3310, 0, 0x04, None, False, 100, "kWh"],
         "YEAR_GENERATED_ENERGY_H": [0x3311, 0, 0x04, None, False, 100, "kWh"],
        "TOTAL_GENERATED_ENERGY_L": [0x3312, 0, 0x04, None, False, 100, "kWh"],
        "TOTAL_GENERATED_ENERGY_H": [0x3313, 0, 0x04, None, False, 100, "kWh"],
                 "BATTERY_VOLTAGE": [0x331A, 2, 0x04, None, False, 100, "V"],
               "BATTERY_CURRENT_L": [0x331B, 0, 0x04, None, False, 100, "A"],
               "BATTERY_CURRENT_H": [0x331C, 0, 0x04, None, False, 100, "A"],
    #### CHARGER SETTINGS ###
                          "RATED_CHARGING_CURRENT": [0x3005, 2, 0x04, None, False, 100, "A"],
                              "RATED_LOAD_CURRENT": [0x300E, 2, 0x04, None, False, 100, "A"],
                      "BATTERY_REAL_RATED_VOLTAGE": [0x311D, 2, 0x04, None, False, 100, "V"],
                                    "BATTERY_TYPE": [0x9000, 0, 0x03, 0x10, False, None, None],
                                "BATTERY_CAPACITY": [0x9001, 0, 0x03, 0x10, False, None, "Ah"],
    "BATTERY_TEMPERATURE_COMPENSATION_COEFFICIENT": [0x9002, 0, 0x03, 0x10, False, 100, "mV/°C/2V"],
          "BATTERY_OVERVOLTAGE_DISCONNECT_VOLTAGE": [0x9003, 2, 0x03, 0x10, False, 100, "V"],
                  "BATTERY_CHARGING_LIMIT_VOLTAGE": [0x9004, 2, 0x03, 0x10, False, 100, "V"],
           "BATTERY_OVERVOLTAGE_RECONNECT_VOLTAGE": [0x9005, 2, 0x03, 0x10, False, 100, "V"],
                    "BATTERY_EQUALIZATION_VOLTAGE": [0x9006, 2, 0x03, 0x10, False, 100, "V"],
                           "BATTERY_BOOST_VOLTAGE": [0x9007, 2, 0x03, 0x10, False, 100, "V"],
                           "BATTERY_FLOAT_VOLTAGE": [0x9008, 2, 0x03, 0x10, False, 100, "V"],
                 "BATTERY_BOOST_RECONNECT_VOLTAGE": [0x9009, 2, 0x03, 0x10, False, 100, "V"],
           "BATTERY_LOW_VOLTAGE_RECONNECT_VOLTAGE": [0x900A, 2, 0x03, 0x10, False, 100, "V"],
           "BATTERY_UNDERVOLTAGE_RECOVERY_VOLTAGE": [0x900B, 2, 0x03, 0x10, False, 100, "V"],
                            "BATTERY_UNDERVOLTAGE": [0x900C, 2, 0x03, 0x10, False, 100, "V"],
          "BATTERY_LOW_VOLTAGE_DISCONNECT_VOLTAGE": [0x900D, 2, 0x03, 0x10, False, 100, "V"],
                 "BATTERY_DISCHARGE_LIMIT_VOLTAGE": [0x900E, 2, 0x03, 0x10, False, 100, "V"],
                     "BATTERY_RATED_VOLTAGE_LEVEL": [0x9067, 0, 0x03, 0x10, False, None, None],
                   "BATTERY_EQUALIZATION_DURATION": [0x906B, 0, 0x03, 0x10, False, None, "Min"],
                          "BATTERY_BOOST_DURATION": [0x906C, 0, 0x03, 0x10, False, None, "Min"],
                         "BATTERY_DISCHARGE_LIMIT": [0x906D, 0, 0x03, 0x10, False, 100, "%"],
                         "BATTERY_DEPTH_OF_CHARGE": [0x906E, 0, 0x03, 0x10, False, 100, "%"],
                           "BATTERY_CHARGING_MODE": [0x9070, 0, 0x03, 0x10, False, None, None],
    #### LOAD PARAMETERS ####
         "LOAD_NIGHT_THRESHOLD_VOLTAGE": [0x901E, 2, 0x03, 0x10, False, 100, "V"],
                     "LOAD_NIGHT_DELAY": [0x901F, 0, 0x03, 0x10, False, None, "min"],
           "LOAD_DAY_THRESHOLD_VOLTAGE": [0x9020, 2, 0x03, 0x10, False, 100, "V"],
                       "LOAD_DAY_DELAY": [0x9021, 0, 0x03, 0x10, False, 100, "min"],
                    "LOAD_CONTROL_MODE": [0x903D, 0, 0x03, 0x10, False, None, None],
                 "LOAD_LIGHT_ON_TIME_1": [0x903E, 0, 0x03, 0x10, False, None, None],
                 "LOAD_LIGHT_ON_TIME_2": [0x903F, 0, 0x03, 0x10, False, None, None],
          "LOAD_TURN_ON_TIME_1_SECONDS": [0x9042, 0, 0x03, 0x10, False, None, "s"],
          "LOAD_TURN_ON_TIME_1_MINUTES": [0x9043, 0, 0x03, 0x10, False, None, "min"],
            "LOAD_TURN_ON_TIME_1_HOURS": [0x9044, 0, 0x03, 0x10, False, None, "h"],
         "LOAD_TURN_OFF_TIME_1_SECONDS": [0x9045, 0, 0x03, 0x10, False, None, "s"],
         "LOAD_TURN_OFF_TIME_1_MINUTES": [0x9046, 0, 0x03, 0x10, False, None, "min"],
           "LOAD_TURN_OFF_TIME_1_HOURS": [0x9047, 0, 0x03, 0x10, False, None, "h"],
          "LOAD_TURN_ON_TIME_2_SECONDS": [0x9048, 0, 0x03, 0x10, False, None, "s"],
          "LOAD_TURN_ON_TIME_2_MINUTES": [0x9049, 0, 0x03, 0x10, False, None, "min"],
            "LOAD_TURN_ON_TIME_2_HOURS": [0x904A, 0, 0x03, 0x10, False, None, "h"],
         "LOAD_TURN_OFF_TIME_2_SECONDS": [0x904B, 0, 0x03, 0x10, False, None, "s"],
         "LOAD_TURN_OFF_TIME_2_MINUTES": [0x904C, 0, 0x03, 0x10, False, None, "min"],
           "LOAD_TURN_OFF_TIME_2_HOURS": [0x904D, 0, 0x03, 0x10, False, None, "h"],
                      "LOAD_NIGHT_TIME": [0x9065, 0, 0x03, 0x10, False, None, None],
                     "LOAD_TIME_CHOOSE": [0x9069, 0, 0x03, 0x10, False, None, None],
    "LOAD_DEFAULT_STATE_IN_MANUAL_MODE": [0x906A, 0, 0x03, 0x10, False, None, None],
    #### RTC PARAMETERS ####
    "DEVICE_RTC_SECOND_MINUTE": [0x9013, 0, 0x03, 0x10, False, None, None],
         "DEVICE_RTC_HOUR_DAY": [0x9014, 0, 0x03, 0x10, False, None, None],
       "DEVICE_RTC_MONTH_YEAR": [0x9015, 0, 0x03, 0x10, False, None, None],
    #### DEVICE PARAMETERS ####
    "BATTERY_UPPER_TEMPERATURE_LIMIT": [0x9017, 2, 0x03, 0x10, False, 100, "°C"],
    "BATTERY_LOWER_TEMPERATURE_LIMIT": [0X9018, 2, 0x03, 0x10, True, 100, "°C"],
       "DEVICE_OVERTEMPERATURE_LIMIT": [0x9019, 2, 0x03, 0x10, False, 100, "°C"],
    "DEVICE_OVERTEMPERATURE_RECOVERY": [0x901A, 2, 0x03, 0x10, False, 100, "°C"],
              "DEVICE_BACKLIGHT_TIME": [0x9063, 0, 0x03, 0x10, False, None, "s"],
    #### DEVICE RATED PARAMETERS ####
      "ARRAY_RATED_VOLTAGE": [0x3000, 2, 0x04, None, False, 100, "V"],
      "ARRAY_RATED_CURRENT": [0x3001, 2, 0x04, None, False, 100, "A"],
      "ARRAY_RATED_POWER_L": [0x3002, 0, 0x04, None, False, 100, "W"],
      "ARRAY_RATED_POWER_H": [0x3003, 0, 0x04, None, False, 100, "W"],
    "BATTERY_RATED_VOLTAGE": [0x3004, 2, 0x04, None, False, 100, "V"],
    "BATTERY_RATED_CURRENT": [0x3005, 2, 0x04, None, False, 100, "A"],
    "BATTERY_RATED_POWER_L": [0x3006, 0, 0x04, None, False, 100, "W"],
    "BATTERY_RATED_POWER_H": [0x3007, 0, 0x04, None, False, 100, "W"],
      #"LOAD_RATED_VOLTAGE": [0x300D, 2, 0x04, None, False, 100, "V"],
       "LOAD_RATED_CURRENT": [0x300E, 2, 0x04, None, False, 100, "A"],
      #"LOAD_RATED_POWER_L": [0x300F, 0, 0x04, None, False, 100, "W"],
      #"LOAD_RATED_POWER_H": [0x3010, 0, 0x04, None, False, 100, "W"],
    #### SWITCHES ####
           "SWITCH_CHARGER_ONOFF": [0x0, 0, None, 0x05, False, None, None],
             "SWITCH_OUTPUT_MODE": [0x1, 0, None, 0x05, False, None, None],
     "SWITCH_LOAD_IN_MANUAL_MODE": [0x2, 0, None, 0x05, False, None, None],
    "SWITCH_LOAD_IN_DEFAULT_MODE": [0x3, 0, None, 0x05, False, None, None],
          "SWITCH_LOAD_TEST_MODE": [0x5, 0, None, 0x05, False, None, None],
              "SWITCH_FORCE_LOAD": [0x6, 0, None, 0x05, False, None, None],
       "SWITCH_RESET_TO_DEFAULTS": [0x13, 0, None, 0x05, False, None, None],
        "SWITCH_CLEAR_STATISTICS": [0x14, 0, None, 0x05, False, None, None]
}

def string_list(string):
  # Convert a string to a list of strings
  return string.split(',')

def open_connection(device, slave_address):
 instrument = minimalmodbus.Instrument(device, slave_address)
 instrument.serial.baudrate = 115200
 instrument.serial.bytesize = 8
 instrument.serial.parity = serial.PARITY_NONE
 instrument.serial.stopbits = 1
 instrument.serial.timeout = 1
 instrument.mode = minimalmodbus.MODE_RTU
 instrument.clear_buffers_before_each_transaction = True
 return instrument

def get_value(selected_register, convert):
    address = dict_registers[selected_register][0]
    if convert == True:
        decimals = dict_registers[selected_register][1]
    else:
        decimals = 0
    readcode = dict_registers[selected_register][2]
    writecode = dict_registers[selected_register][3]
    signed = dict_registers[selected_register][4]
    times = dict_registers[selected_register][5]
    unit = dict_registers[selected_register][6]
    if readcode == 1 or readcode == 2:
        response = instrument.read_bit(address, readcode)
    elif readcode == 3 or readcode == 4:
        response = instrument.read_register(
            address, decimals, readcode, signed)
    else:
        response = None
    if unit == None:
        unit = ""
    if times == None:
        times = ""
    if response == None:
        response = ""
    return response, times, unit

parser = argparse.ArgumentParser(
    description='Tool for dumping register values from Epever MPPT chargers via MODBUS RTU.',
    epilog='Example:  dumpreg.py -d /dev/ttyACM0 -c -q ARRAY_VOLTAGE,ARRAY_CURRENT,ARRAY_POWER_L',
)
parser.add_argument('-d', '--device',  type=str, default='/dev/ttyACM0', help='Device to use. Default is /dev/ttyACM0.')
parser.add_argument('-i', '--id',      type=int, default=1, help='Modbus slave address. Numeric value. Default is 1.')
parser.add_argument('-l', '--list',    action='store_true', help='List all known registers with their labels and details.')
parser.add_argument('-a', '--all',     action='store_true', help='Probe all known readable registers.')
parser.add_argument('-q', '--query',   type=string_list,    help='Query selected registers. List of labels separated by commas.')
parser.add_argument('-c', '--convert', action='store_true', help='Output with decimals, calculation and units. Computes _L and _H together and modifies output register name.')
parser.add_argument('--version', action='version', version='0.1')

# Parse the command-line arguments
args = parser.parse_args()

if args.list:
    for selected_register, value in dict_registers.items():
     print(f"{selected_register}: [address={hex(value[0])}, decimals={value[1]}, readcode={value[2]}, writecode={value[3]}, signed={value[4]}, times={value[5]}, unit={value[6]}]")
    exit(0)

# Use default value for --device if not specified
if args.device:
    device = args.device
else:
    device = '/dev/ttyACM0'
#print(f'Using device: {device}')

# Check if device file exists
if not os.path.exists(device):
    print("Error: File", device, "does not exist. Exiting.")
    print("Try running command 'sudo dmesg -w' and reconnect cable.")
    print("On Linux, you should see new device attached as /dev/ttyUSB0 or /dev/ttyACM0.")
    exit(1)

# Use default value for --id argument if not specified
slave_address = args.id
convert = args.convert

if args.all:
    instrument = open_connection(device, slave_address)
    for selected_register, value in dict_registers.items():
        if convert == True:
            if selected_register.endswith("_L"):
                selected_register_base = selected_register[:-2]
                response_l, times, unit = get_value(selected_register_base + "_L", convert)
                response_h, times, unit = get_value(selected_register_base + "_H", convert)
                response = (response_h << 16) | response_l
                print(selected_register_base, "=", response / times, unit)
            elif selected_register.endswith("_H"):
                pass
            else:
                response, times, unit = get_value(selected_register, convert)
                print(selected_register, "=", response, unit)
        else:
            response, times, unit = get_value(selected_register, convert)
            print(selected_register, "=", response)
    exit(0)


if args.query:
    if len(args.query) > 0:
        instrument = open_connection(device, slave_address)
        for selected_register in args.query:
            if convert == True:
                if selected_register.endswith("_L") or selected_register.endswith("_H"):
                    selected_register_base = selected_register[:-2]
                    response_l, times, unit = get_value(selected_register_base + "_L", convert)
                    response_h, times, unit = get_value(selected_register_base + "_H", convert)
                    response = (response_h << 16) | response_l
                    print(selected_register_base, "=", response / times, unit)
                else:
                    response, times, unit = get_value(selected_register, convert)
                    print(selected_register, "=", response, unit)
            else:
                response, times, unit = get_value(selected_register, convert)
                print(selected_register, "=", response)
        exit(0)
    else:
        print("Error: Not enough elements in query list")
        exit(1)

'''
BATTERY_TYPE = 7 equals LiFePo4 16s in XTRA 4415N.
'''
