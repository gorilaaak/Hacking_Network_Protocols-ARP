#!/usr/bin/env python
import optparse
import scapy.all as scapy
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", type='str', dest="target", help="Target IP / Subnet mask f.e 192.168.100.0/24")
    (options, _) = parser.parse_args()
    if not options.target:
        #code to handle error with Interface
        parser.error("[-] Please specify an target subnet address and subnet mask, use --help for more info")
    return options

def scan (ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    ans_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in ans_list:
        client_dict = {"IP": element[1].psrc, "MAC": element[1].hwsrc}
        client_list.append(client_dict)
    return (client_list)

def print_result(results_list):
    print("Running ARP scan of: % s" % options.target)
    print()
    print("IP\t\t\tMAC Address\n--------------")
    for client in results_list:
        print(client["IP"] + "\t\t" + client["MAC"])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)




