
# -*- coding: utf-8 -*-
import sys
import time
import binascii
import can
import logging
from datetime import datetime

# Настройка логирования с указанием формата временной метки
logging.basicConfig(filename='can_logging.log', level=logging.INFO, format='%(message)s',filemode='w')

bus1 = can.interface.Bus(channel='can0', interface='socketcan')
bus2 = can.interface.Bus(channel='can1', interface='socketcan')

uds_data = {
    "150 01": [0x00, "10 04 00 00 00 00 00 00"],
    "negative": ["01 02 03 04 05 06 07 08"]
}

data = {
    "150 01": [0x00, "10 04 00 00 00 00 00 00"],
    "negative": ["01 02 03 04 05 06 07 08"]
}

pid = ""
commands_to_send = [
#    {"bus": bus1, "id": 0x7E8, "data": "01 02 03 04 05 06 07 08", "extended": False},
#    {"bus": bus1, "id": 0x1FF, "data": "11 12 13 14 15 16 17 18", "extended": False},
#    {"bus": bus2, "id": 0x7E8, "data": "21 22 23 24 25 26 27 28", "extended": True},
#    {"bus": bus2, "id": 0x1ABCDE, "data": "31 32 33 34 35 36 37 38", "extended": True},

    {"bus": bus1, "id": 0x150, "data": "00 00 00 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x150, "data": "01 00 00 00 00 00 00 00", "extended": False},    
    {"bus": bus1, "id": 0x160, "data": "01 FF 00 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "01 FF 01 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "01 FF 02 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "01 FF 03 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "01 FF 03 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "01 FF 02 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "01 FF 01 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "01 FF 00 00 00 00 00 00", "extended": False},
    {"bus": bus1, "id": 0x160, "data": "00 00 00 00 00 00 00 00", "extended": False},
#    {"bus": bus2, "id": 0x1, "data": "10 04 00 00 00 00 00 00", "extended": True},
#    {"bus": bus2, "id": 0x2, "data": "10 04 00 00 00 00 00 01", "extended": True},
#    {"bus": bus2, "id": 0x3, "data": "10 04 00 00 00 00 00 00", "extended": True},
#    {"bus": bus2, "id": 0x4, "data": "10 04 00 00 00 00 00 01", "extended": True},
]

def log_message(action, bus_name, arbitration_id, message, is_extended):
    """Функция для логирования сообщений с временной меткой и типом пакета."""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Only time, no date
    message_type = "Extended" if is_extended else "Standard"
    logging.info(f"{current_time} - {action:<8} on {bus_name}: ID: {hex(arbitration_id):<10} {message_type} Data: {binascii.hexlify(message, ' ')}")

def send_can2_id(id, message):
    msg = can.Message(arbitration_id=id, data=bytes.fromhex(message), is_extended_id=True)
    #bus2.send(msg)
    log_message("Sent____", "bus2", msg.arbitration_id, msg.data)
def send_commands(commands):
    for command in commands:
        # Создание CAN-сообщения
        msg = can.Message(arbitration_id=command["id"], 
                          data=bytes.fromhex(command["data"]), 
                          is_extended_id=command["extended"])
        # Отправка сообщения на соответствующую CAN-шину
        command["bus"].send(msg)
        # Логирование или вывод информации о переданном сообщении
        id_type = "Extended" if command["extended"] else "Standard"
        print(f"Sent: ID={hex(command['id'])} [{id_type}] Data={command['data']}")
        # Логирование
        bus_name = "bus1" if command["bus"] == bus1 else "bus2"
        log_message("Sent____", bus_name, command["id"], msg.data, msg.is_extended_id)
        # Задержка между отправками
        time.sleep(0.5)
class CanListener1(can.Listener):
    def on_message_received(self, message):
        global pid
        log_message("Received", "bus1", message.arbitration_id, message.data, message.is_extended_id)
        print(hex(message.arbitration_id), binascii.hexlify(message.data, " "))

class CanListener2(can.Listener):
    def on_message_received(self, message):
        global pid
        log_message("Received", "bus2", message.arbitration_id, message.data, message.is_extended_id)
        print(hex(message.arbitration_id), binascii.hexlify(message.data, " "))
if __name__ == "__main__":
    listener1 = CanListener1()
    listener2 = CanListener2()
    notifire1 = can.Notifier(bus1, [listener1])
    notifire2 = can.Notifier(bus2, [listener2])
    send_commands(commands_to_send)
    time.sleep(1)
    bus1.shutdown()
    bus2.shutdown()
   # notifire1.stop()
   # notifire2.stop()
    sys.exit(0)
    while True:
        pass
