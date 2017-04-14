# DHCP_VLSM-Server
DHCP server is implemented using VLSM method. Language used is python.
Server reads a file 'subnets.conf' in which the main ip is given with the strength of labs and names.
Also there are some MAC addresses given corresponding to labs.
Server assigns Network Addresses and Broadcast Addresses to labs and ask MAC address from the client to give corresponding ip to the client.
To run the server open the folder "server" and run "./server".
To run the client open the "client" folder and run either "./client" or "./client -m <MAC Address>",in the former case it will automatically read system's MAC address.
 
