# MITM-Demo

This is a demonstration of man-in-the-middle (MITM) attack.

A socket communication is established between a server RPi and client RPi. A third party system (laptop) in the network can read and modify the data by first running the ARP Spoofer and then the MITM Attacker.
ARP Spoofer modifies the ARP tables of the client and server, thereby rerouting the traffic through the laptop.
The MITM attacker routes the traffic in the laptop through NFQUEUE so that packets can be read and modified.

The client RPi is toggling button1 and button2 of server RPi. The MITM attacker modifies the switch number before rerouting the data to server.

Requirements:
Ubuntu,
Python 3

Libraries to be installed:
Scapy,
NetfilterQueue

Credits:
This code has derived and modified the codes from https://github.com/x4nth055/pythoncode-tutorials/tree/master/scapy/arp-spoofer and https://github.com/johnnymythology/Man-In-The-Middle-Packet-Manipulation.git for this specific case scenario. 

