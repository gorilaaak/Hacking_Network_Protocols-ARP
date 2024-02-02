# Hacking Network Protocols: ARP

In this lab ill explain what is ARP and introduce some popular hacks against this protocol.

# Part 1: ARP Overview

ARP is not known by most people, yet today’s network’s cannot work without it at all - at least IPv4 network’s. In simple terms ARP is matching the MAC address with IP address on the local network, Lets understand the MAC address first.

## MAC address

or Medium-Access-Control better known as physical/hardware address is unique identifier assigned to network interface which is a fundamental part of Ethernet and other IEEE 802 networking standards. Ethernet is a widely used networking technology that defines the physical and data link layers of the OSI (Open Systems Interconnection) model. It provides a framework for connecting computers and other devices within a local area network (LAN) 

Ethernet is simply a standard for communication MAC addresses are typically assigned by the manufacturer of the network interface controller (NIC) and are stored in its hardware. Every device which desire to communicate via TCP/IP stack needs to have MAC address. 

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled.png)

MAC address is 48-bit - first half (24 bits) OUI - Organizationally Unique Identifier (OUI), assigned to the manufacturer by the IEEE (Institute of Electrical and Electronics Engineers). The second half (24 bits) is the Network Interface Controller (NIC) Specific, which is assigned by the manufacturer to uniquely identify the network interface. 

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%201.png)

MAC encapsulates data into so called **frames.** Frames are L2 PDU - Protocol Data Unit - fancy word for types of packet’s used by particular layer of TCP/IP. Frame contains source and destination MAC address of the device’s which are sending frames and also where the frame is destined - very similar to packet where we need to specify the source and destination IP. In picture below you can see how the Ethernet frame is structured - we not gonna into more detail here so we will focus on source and destination MAC mainly.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%202.png)

Lets observe MAC address from Wireshark by simply sending pings from client PC to Router.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%203.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%204.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%205.png)

## Changing MAC address?

MAC address is crucial for technology such Wi-Fi which uses various types of frames but one special called **probe request**. Probe request is sent by station (client) on regular basis due scanning for available AP’s. Wi-Fi heavily relies on broadcasts and management frames (such probe request) are not encrypted hence anyone capable of capturing frames from the air can observe client MAC address and spoof it. Smartphones are most impactful technology today - this is why mobile devices changing or obfuscating MAC address on regular basis to add layer of security. Altering the MAC address on the fly is however challenge with using access list’s where we black/white list the MAC where we specify the particular MAC for access/denial.

Altering the MAC address - by changing the 2nd least bit in the first octet of the MAC address. 

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%206.png)

## How Data is send?

Now we have two types of addresses - IP address which is known for most people and MAC address. Each one of these is operating on different OSI Layer. MAC is L2 and IP is L3. The actual data transfer is happening on L2. Why? Because L2 represents devices which are **directly** connected within same LAN in some way. But okay but how to do we access our favorite website on the Internet which is outside of our LAN? Lets examine the simple NW topology below

Here Client Host wants to visit Web server hosting website on the Internet - by using IP address. But IP address is an **logical** connection - means we are able to establish connection even over-Sea from our cozy household by any second. As we can see every Link (usually called **hops**) from our home to the Internet server is **direct** connection - means our frame which is holding data will traverse every physical segment (network) to get to the Internet server and back. This is why we need IP addresses - to interconnect multiple LAN’s and we need MAC’s to deliver data. 

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%207.png)

## Address Resolution

Important part of this process which we understood earlier about sending data is Address resolution. It is a method to pair the logical address (IP address ) and hw address (MAC address) - because as we understood earlier - internetworked devices communicate logically using L3 address (IP) but the actual transmission is taking place at L2 - using MAC address.

**Important !!!**

To avoid confusion I mentioned IP address is used by internetworked devices to establish logical connection and exchange data - this is true but IP is also used on LAN where all devices may be directly connected - this is because we are using TCP/IP model where IP is main protocol for data exchange and delivery.

We have two types of address resolution - static (direct mapping) and dynamic. We will omit diving into static resolution for now and focus on dynamic resolution. To understands this lets use simple analogy:

You've probably witnessed airport limo drivers, even if only in movies. Our situation is quite similar: they have a passenger's name but not their face, like a "local address" puzzle. To locate the passenger, they display a sign with the name, hoping the right person will spot it and come forward, while others ignore it.

We employ a similar concept in dynamic address resolution within a network. Consider device A wishing to communicate with device B but having only device B's IP address (its "name") and not its MAC address (its "face"). Device A broadcasts a layer two frame that carries device B's layer three address, similar to displaying a card with someone's name on it. Devices other than B do not identify this layer three address and disregard it. Device B, however, recognizes its own network layer address within the broadcast frame and responds directly to device A. This communication reveals device B's layer two address, completing the address resolution process.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%208.png)

## ARP

Address Resolution Protocol (ARP) is the key address resolution protocol within TCP/IP. ARP  is a comprehensive dynamic resolution protocol employed to associate IP addresses with underlying data link layer addresses. Basic operation of ARP is a request/response pair of transmissions on the local network, but without unicast (exact IP address) addressing ARP needs first to send **broadcast** frame to network - which means everyone on the network will receive the frame. 

Overview of ARP process.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%209.png)

Okay, in theory we covered ARP fair enough - lets see basic ARP in action. I will be using GNS3 with very basic topology.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2010.png)

Since ARP rely on broadcast’s is very un-efficient to send ARP frames each time we need to perform address resolution. Time to meet ARP table - ARP table is type of simple cache which is used to store address resolution’s to facilitate whole process . Lets see ARP table in PC1

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2011.png)

As we can see we have IP and MAC address of our Router stored in ARP cache, lets clear it out, send few packets towards Router and capture traffic with Wireshark.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2012.png)

We can already see the ARP is taking place, PC1 is sending request as Broadcast to all parties in the network to look for 10.0.0.1, few seconds after response is sent back, also ARP table is updated with fresh record.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2013.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2014.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2015.png)

# Part 2: Hacking ARP

**!!! DISCLAIMER - this section is dedicated to some of the common ARP attacks. Performing these attacks are only for educational purposes. I am performing these attacks in the isolated lab which i own and manage. DO NOT PERFORM this type of attacks on any network which you do not own otherwise this will be considered illegal, un-ethical and may result in pressing charges and coliding with authorities in particullar organization or state.**

Understanding ARP is crucial to recognize its vectors - there are two major - ARP is using broadcast so the frame is received and processed by every device in the LAN and ARP messages are un-encrypted means we can perform a pretty easy reconnaissance. ARP hacking is very popular in public Wi-Fi networks such coffee shops or anywhere where the access to the network is free most of the time or very poorly secured - and we do not need to be inside the Wi-Fi network to gather basic info since Wi-Fi is broadcasting un-encrypted management frames all the time. Lets gear up:

Our setup is previous GNS3 lab + Kali Rogue PC - easy, lets have some fun.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2016.png)

## Script kiddie?

Okay, we will pause here a bit. In latest projects we relied heavily on tools provided by Kali-distro. Is convenient to use tool for a job, also in many cases is mandatory - but those who rely heavily on pre-loaded tools are called script kiddies - we will break out from this and create our own. We will create two simple programs:

- ARP scanner
- ARP spoofer

We will use these programs to demonstrate ARP hacking. We will use Python and library called scapy - library which allow us to manipulate and send packets - see documentation for more:

[https://scapy.readthedocs.io/en/latest/index.html](https://scapy.readthedocs.io/en/latest/index.html)

## ARP scanner

We need to start from beginning and perform some basic reconnaissance - for short recon is method of gathering pieces of information about possible targets. Since ARP is relying on broadcast packets, we can subvert this design to perform easy recon or scan on our LAN. 

We will create ARP scanner by using Python and scapy to send the ARP packets to the target network. Scapy comes with **arping** pre-loaded function - function is just a block of reusable code. **arping** will perform very basic ARP scan.

Lets check our network details and fire up Python3 console and use **arping**. Also run the Wireshark in background.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2017.png)

As we can see arping sends ARP request for every IP address in the network, we can already see devices replying with IP addresses and MAC addresses.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2018.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2019.png)

Okay, but this method isn’t really convenient and we are still using pre-built tool - lets use Python to write simple ARP scanner - i am not gonna guide you through the process, you can check the code in the repo.

Once the code is done lets retry and fire up wireshark to capture the process.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2020.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2021.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2022.png)

Very good, our code works as expected and we successfully scanned the network for potentional targets.

## ARP spoofer

In ARP spoofing attack, malicious actor send false ARP messages to associate their own MAC address with the IP address of another device, often a gateway or router. This can redirect traffic through the attacker's machine, allowing for eavesdropping, interception, or manipulation of data. This attack is possible because ARP operates without strong authentication or verification mechanisms, making it susceptible to manipulation. Issue is we can send ARP response without request which means the target will accept and process the reply, because ARP is simple protocol without any security measures.

Now lets construct an ARP response to fool client PC - using scapy and Python one liner. Lets start with recon using our previous ARP_scanner.  As we can see that we have three possible victims, minus 10.0.0.1 which is our gateway.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2023.png)

Lets verify the details first on client PC - PC has associated MAC with IP of the Router.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2024.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2025.png)

Now run the Python interpreter and construct simple ARP response with scapy. In summary we can see what this packet will do - it will send an ARP response to PC 1 originates from R1 IP address but instead R1 MAC address it will put ours. Finally once constructed lets start Wireshark and send the packet.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2026.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2027.png)

Once done lets check arp table on the PC1 - as we can see PC1 associated both IP addresses with the same MAC. 

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2028.png)

But this approach is not very useful - once we access the web again MAC address of default gateway is restored back to original - it is because we are sending only one response.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2029.png)

In order to run the ARP spoofing attack constantly i have constructed a script which will send countless of ARP replies - similar the way we sent it in previous section -  to client and gateway which will puts us in the middle. Once we stop the attack the script will automatically restore the previous ARP cache mapping. Lets again scan the network for potential targets and run the spoofer against client and gateway.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2030.png)

### Important !!!

Since we are passing network traffic from one device to another we need to have ipv4-forwarding setup - type the command below before starting the ARP spoofer.

**echo 1 > /proc/sys/net/ipv4/ip_forward**

Okay our attack is running - lets run Wireshark on the Kali machine and lets test ping from victim machine to verify.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2031.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2032.png)

Now we are in the middle. No we know our Router is running the http service to be accessible from web - lets try to connect from the PC1 while we are spoofing the traffic.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2033.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2034.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2035.png)

We successfully captured the credentials. Lets try to connect to the Router once again. Note that we have admin access it means full access to disrupt the network.

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2036.png)

![Untitled](Hacking%20Network%20Protocols%20ARP%204308810d6b6c4cf5bf76b152e7f36a3c/Untitled%2037.png)

Success, now we are able to disrupt the network from inside. 

# Wrap up

As you could see ARP spoofing is pretty easy attack to perform even with few lines of code or with tools like Ettercap. How to mitigate such attacks? Some antivirus software such ESET does have IDS/IPS built in - IPS and IDS are tools to prevent and detect network anomalies such ARP spoofing.

One way is to setup this tool on end-user machine such PC or Smartphone but i larger organizations there are tools such Snort which can be setup to perform pro-active monitoring and logging of such anomalies on the network.

# Resources:

**The TCP-IP Guide - A Comprehensive Illustrated Internet Protocols Reference**

[https://github.com/akib1162100/mac/blob/master/The TCP-IP Guide - A Comprehensive Illustrated Internet Protocols Reference.pdf](https://github.com/akib1162100/mac/blob/master/The%20TCP-IP%20Guide%20-%20A%20Comprehensive%20Illustrated%20Internet%20Protocols%20Reference.pdf)

**Black Hat Python**

[https://www.amazon.com/dp/1718501129/](https://www.amazon.com/dp/1718501129/)