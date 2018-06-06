from scapy.all import conf,srp,Ether,ARP,send,sniff,wrpcap
#import pcap
import time
import os
import sys
import threading
import signal

# define ip addressess, packet count, interface name

interface = "eth0"
gateway_ip = "192.168.0.1"
target_ip = "192.168.0.100"
packet_count = 1000
poisoning = True

#TODO define restore_target
def restore_target(gateway_ip, target_ip, gateway_mac, target_mac):
    print "**Restoring target now...**"

    # op =2 issues ARP reply, psrc is the source gateway ip, pdst is the source host. hwdst ="ff:ff:..." identifies
    # packets addressesd to every computer on a lan segment. ether frames containing IP broadcast packages also
    # typically sent to this address. hwsrc identifies the physical address of the gateway
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

    print " Systems restored - exiting..."

#TODO define get_mac
def get_mac(ip_address):
    # send/receive packages on ethernet w/ dest "ff:ff:..."
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None
#TODO define poison_target

#TODO define body

