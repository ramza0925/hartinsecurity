import socket
import struct

def dump_hex(string):
	return " ".join(x.encode('hex') for x in string)
	
def dump_wireshark(string):
	(hart, j) = get_packet_data(string)
	
	ln  = 253
		
	ln = min(len(hart), ln)
	
	hartip = '\x01\x01\x03\x00\x00\x03' + '\x00' + chr(ln) + hart
	
	# uncomment to dump packet through network
	#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
	#s.sendto(hartip, ('172.16.0.161', 5094))
	
def get_packet_data(packet):
	for i in xrange(0, len(packet)):
		if packet[i] != '\xff':
			break
			
	return (packet[i:-1], i)
	
def pack_ascii(text):
	i = 0
	retstr = ""

	while(i+4 <= len(text)):
		ret = [0,0,0]
		ret[0] = (ord(text[i]) << 2) & 252
		ret[0] = ret[0] | (((ord(text[i+1]) << 2) & 192) >> 6 )

		ret[1] = (ord(text[i+1]) << 4) & 240
		ret[1] = ret[1] | (((ord(text[i+2]) << 2) & 240) >> 4)
		
		ret[2] = ((ord(text[i+2]) << 6) & 192) | (ord(text[i+3]) & 0x3F)
	
		i = i + 4
		
		retstr = retstr + chr(ret[0]) + chr(ret[1]) + chr(ret[2])
		
	#if(i < len(text)):
	#	ret = ret + "\x00"
		
	while(i < len(text)):
		retstr = retstr + text[i]
		i = i + 1
		
	return retstr


def get_packet(delimiter, address, preambles, command, response, status, data, length = -1000):
	ln  = 253
	
	ln = min(len(data), ln)
	ln = ln + 2

        if length != -1000:
		ln = length
	
	pack = chr(delimiter) + address + chr(command) + chr(ln) + chr(response) + chr(status) + data 
	return '\xff' * preambles + pack + get_checksum(pack)
	
def get_checksum(data):
	
	chk = ord(data[0])
	
	for i in range(1,len(data)):
		chk = chk ^ ord(data[i])
		
	return chr(chk)


class hart_slave_protocol:
	
	manufacturer_id = "\x01"
	device_type = "\x01"
	device_revision = "\x01"
	software_revision = "\x01"
	hardware_revision = 0
	uniq_address = '\x43\x43\x43\x43\x43'
	bus_address = 0
		
	def __init__(self):
		pass
	
	def command0(self, master_preambles, hart_revision, signal_code, flags, devid, slave_preambles, devvars, configchange):
		cmd = '\xfe' # byte 0
		cmd = cmd + self.manufacturer_id
		cmd = cmd + self.device_type
		cmd = cmd + chr(master_preambles)
		cmd = cmd + chr(hart_revision)
		cmd = cmd + self.device_revision
		cmd = cmd + self.software_revision
		cmd = cmd + chr((self.hardware_revision << 3) & 248 + signal_code)
		cmd = cmd + chr(flags)
		cmd = cmd + devid
		cmd = cmd + chr(slave_preambles)
		cmd = cmd + chr(devvars)
		cmd = cmd + chr(configchange)
		
		return cmd
	
	def command13(self, tag, description, day, month, year):
		return pack_ascii(tag) + pack_ascii(description) + chr(day) + chr(month) + chr(year)
		
	def command1(self, type, float):
		return chr(type) + struct.pack('f', float)
		
	def command2(self, current, percentage):
		return struct.pack('f', current) + struct.pack('f', percentage)
		
	def command3(self, current, var1t, var1, var2t, var2, var3t, var3, var4, var4t):
		return struct.pack('f', current) + chr(var1t) + struct.pack('f', var1) + chr(var2t) + struct.pack('f', var2) + chr(var3t) + struct.pack('f', var3) + chr(var4t) + struct.pack('f', var4)
		
	def command15(self, alarm, pvtransfer, pvrangecode, pup, pdown, pdamp, protectcode, labelcode, channelflags):
		cmd = ""
		cmd = cmd + chr(alarm) + chr(pvtransfer) + chr(pvrangecode) 
		cmd = cmd + struct.pack('f', pup) + struct.pack('f', pdown) + struct.pack('f', pdamp)
		cmd = cmd + chr(protectcode) + chr(labelcode) + chr(channelflags)	
		return cmd