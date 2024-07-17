import time
import argparse
from pyiec61850 import IEC61850Client, MMSNamedVariableList, MMSValue, DataType, ClientException

def send_sv_message(destination_ip, port):
    try:
        client = IEC61850Client(destination_ip, port)
        client.connect()

        sv_message = MMSNamedVariableList()
        sv_message.add('IEDName/LLN0$GO$GOOSE', MMSValue(DataType.STRING, 'SV Message Content'))
        client.write(sv_message)

        print("SV message sent to {}:{}".format(destination_ip, port))
        client.disconnect()
    except ClientException as e:
        print("Failed to send SV message: ", str(e))

def send_goose_message(destination_ip, port):
    try:
        client = IEC61850Client(destination_ip, port)
        client.connect()

        goose_message = MMSNamedVariableList()
        goose_message.add('IEDName/LLN0$GO$GOOSE', MMSValue(DataType.STRING, 'GOOSE Message Content'))
        client.write(goose_message)

        print("GOOSE message sent to {}:{}".format(destination_ip, port))
        client.disconnect()
    except ClientException as e:
        print("Failed to send GOOSE message: ", str(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send SV and GOOSE messages')
    parser.add_argument('destination', type=str, help='Destination IP address')
    parser.add_argument('port', type=int, help='Destination port')
    parser.add_argument('--sv', action='store_true', help='Send SV message')
    parser.add_argument('--goose', action='store_true', help='Send GOOSE message')
    args = parser.parse_args()

    if args.sv:
        send_sv_message(args.destination, args.port)
    if args.goose:
        send_goose_message(args.destination, args.port)
