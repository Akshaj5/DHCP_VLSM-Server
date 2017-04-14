import socket
import os,sys,re
from datetime import *
import random
import copy
import threading,time




def powof2(arr,count,num):
	for i in range(len(arr)):
		k = arr[i]+2
		for j in range(0,33):
			if 1<<j >= k:
				num.append(1<<j)
				count.append(j)
				break



def bubble_sort(labs,items,count):
    """ Implementation of bubble sort """
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j] < items[j+1]:
				items[j], items[j+1] = items[j+1], items[j]
				labs[j], labs[j+1] = labs[j+1], labs[j]
				count[j], count[j+1] = count[j+1], count[j]


def netadd(items,ba):
	mask = items[4]
	for i in range(len(items)-1):
		if mask >= 8:
			items[i] = items[i] & 255
			mask = mask-8
			ba.append(items[i])
		else:
			for j in range(1,9):
				if mask == 8-j:
					l = 255-(1<<j)+1
					items[i] = items[i] & l
					mask = mask - (8-j)
					k = items[i]+(1<<j) -1
					ba.append(k)
					break
	ba.append(items[4])


def add(address):
	add = copy.deepcopy(address)
	for i in [3,2,1,0]:
		if(add[i]+1 > 255):
			add[i] = 0
		else:
			add[i] = add[i]+1
			break
	return add


def sub(address):
	add = copy.deepcopy(address)
	for i in [3,2,1,0]:
		if(add[i] == 0):
			add[i] = 255
		else:
			add[i] = add[i] - 1
			break
	return add

#def findlab(temp):


def vlsm(count,majorna,list_of_na,list_of_ba):
	for i in count:
		if (majorna[4] > 32 -i):
			print "Error: Too many hosts,cannot allocate ip addresses"
			exit(0)
		majorna[4] = 32 - i
		subnetba = []
		netadd(majorna,subnetba)
		list_of_na.append(majorna)
		list_of_ba.append(subnetba)
		majorna = add(subnetba)
	return majorna


def search(mac,lines,labs,majorna,assign,list_of_na,unreg_mac,lab_no,num,other):
	flag =0
	lab_no[0] = -1
	for i in lines:
		y = i.split(" ")
		if(y[0]==mac):
			for j in range(len(labs)):
				if(y[1]==labs[j]):
					flag = 1
					lab_no[0] = j
					break

	if(flag ==1):
		assign[lab_no[0]] += 1
		g = 1
		addrs = list_of_na[lab_no[0]]
		while g <= assign[lab_no[0]]:
			addrs = add(addrs)
			g += 1
		return addrs

	elif(flag==0):
		if(other != 0):
			for i in range(len(labs)):
				if labs[i] == "other":
					if((num[i]-3) == assign[i]):
						error = []
						error.append("Error:")
						error.append("No more ip left for unregistered MAC addresses")
						return error
					lab_no[0] = i
					assign[i] += 1
					h = 1
					addrs = list_of_na[i]
					while h<= assign[i]:
						addrs = add(addrs)
						h += 1
					return addrs
		elif(other == 0):
			#print "akshaj"
			error = []
			error.append("Error:")
			error.append("No more ip left for unregistered MAC addresses ")
			return error




port= 60024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""

s.bind((host, port))
s.listen(5)





print 'Server listening....'

with open("subnets.conf") as f:
    lines = f.readlines()
lines = [x.strip() for x in lines]


a = lines[0].split('.')
b = a[3].split('/')
majorip = []
majorip.append(int(a[0]))
majorip.append(int(a[1]))
majorip.append(int(a[2]))
majorip.append(int(b[0]))
majorip.append(int(b[1]))

majorba = []
majorna = copy.deepcopy(majorip)
netadd(majorna,majorba)


i = 1
labs = []
capacity = []
no_of_labs = int(lines[1])
assign = []
while i <= no_of_labs :
	j = lines[i+1].split(':')
	k = int(j[1])
	capacity.append(k)
	labs.append(j[0])
	assign.append(0)
	i += 1

count = []
num = []
powof2(capacity,count,num)
total_capacity = 1 << (32 - int(b[1]))
#print total_capacity
other = total_capacity
for i in range(len(num)):
	other = other - num[i]

if(other < 0):
	print "Error: Too many hosts,cannot allocate ip addresses"
	exit(0)


if(other > 0): 
	for i in range(0,33):
		if 1<<i > other:
			num.append(1<<(i-1))
			count.append(i-1)
			labs.append('other')
			assign.append(0)
			break

bubble_sort(labs,num,count)

list_of_na = []
list_of_ba = []

unreg_mac = []
unreg_mac.append(0)

majorna = vlsm(count,majorna,list_of_na,list_of_ba)
if(other != 0):
	for i in range(len(labs)):
		if labs[i] == "other":
			server_ip = sub(list_of_ba[i])
else:
	server_ip = sub(list_of_ba[0])

print "Server IP is:",str(server_ip[0])+str(".")+str(server_ip[1])+str(".")+str(server_ip[2])+str(".")+str(server_ip[3])+str("/")+str(server_ip[4])

for i in range(len(labs)):
	#if(labs[i] == 'other'):
	#	continue
	print "The N.A. for lab",labs[i],"is:",str(list_of_na[i][0])+str(".")+str(list_of_na[i][1])+str(".")+str(list_of_na[i][2])+str(".")+str(list_of_na[i][3])
	print "The B.A. for lab",labs[i],"is:",str(list_of_ba[i][0])+str(".")+str(list_of_ba[i][1])+str(".")+str(list_of_ba[i][2])+str(".")+str(list_of_ba[i][3])


#print ip
dic_maci={}
dic_macna={}
dic_macba={}
dic_macgate={}
dic_macDNS={}


while True:
	try :
		conn,addr = s.accept()
		mac = conn.recv(1024)
		#mac = "F8:D0:90:80:65:A8"
		if mac in dic_maci:
			tempi=dic_maci[mac]
			tempna=dic_macna[mac]
			tempba=dic_macba[mac]
			tempgate=dic_macgate[mac]
			tempDNS=dic_macDNS[mac]

			temp=tempi+tempna+tempba+tempgate+tempDNS

			conn.send(temp)
		else:
			lab_no = []
			lab_no.append(-1)
			ip = search(mac,lines,labs,majorna,assign,list_of_na,unreg_mac,lab_no,num,other)
			#print ip
			#print lab_no[0]
			#print "akshaj"
			if (ip[0] == "Error:"):
				#print "akshaj"
				temp = str(ip[0])+str(ip[1])+"\n"

			else:	
				tempi=str("IP address is:        ")+str(ip[0])+"."+str(ip[1])+"."+str(ip[2])+"."+str(ip[3])+"/"+str(ip[4])+"\n"
				tempna=str("Network address is:   ")+str(list_of_na[lab_no[0]][0])+str(".")+str(list_of_na[lab_no[0]][1])+str(".")+str(list_of_na[lab_no[0]][2])+str(".")+str(list_of_na[lab_no[0]][3])+ "\n"
				tempba=str("Broadcast address is: ")+str(list_of_ba[lab_no[0]][0])+str(".")+str(list_of_ba[lab_no[0]][1])+str(".")+str(list_of_ba[lab_no[0]][2])+str(".")+str(list_of_ba[lab_no[0]][3])+"\n"
				tempgate=str("Sample Gateway is:    ")+str(list_of_ba[lab_no[0]][0])+str(".")+str(list_of_ba[lab_no[0]][1])+str(".")+str(list_of_ba[lab_no[0]][2])+str(".")+str(list_of_ba[lab_no[0]][3]-1)+"\n"
				tempDNS=str("Sample DNS is:        ")+str(list_of_ba[lab_no[0]][0])+str(".")+str(list_of_ba[lab_no[0]][1])+str(".")+str(list_of_ba[lab_no[0]][2])+str(".")+str(list_of_ba[lab_no[0]][3]-1)+"\n"
				temp=tempi+tempna+tempba+tempgate+tempDNS

				dic_maci[mac]=tempi
				dic_macna[mac]=tempna
				dic_macba[mac]=tempba
				dic_macgate[mac]=tempgate
				dic_macDNS[mac]=tempDNS


			conn.send(temp)
	except:
		s.close()
		exit(0)
