import serial,time,socket
import hart_protocol
import sys

port = 3

if len(sys.argv) >= 2:
	port = int(sys.argv[1]) - 1

print "Opening COM" + str(port + 1) + "..."

hs = hart_protocol.hart_slave_protocol()

hs.manufacturer_id = "\xe0"
hs.device_type = "\xbd"
hs.hardware_revision = 1
hs.device_revision = "\x03"
hs.bus_address = 0

preambles = 5
	
ser = serial.Serial(port, 1200)

while True:
	n = ser.inWaiting()
	packet = ""
	
	if n > 0:
		packet = ser.read(n)
		
		print "__RCVD__: " + hart_protocol.dump_hex(packet)
				
		(payload, preambles) = hart_protocol.get_packet_data(packet)
		if payload[2] == '\x00':
			print "recv: command 0 for " + str(ord(payload[1]) % 128)
			
			# command 0
			newpacket = hs.command0(preambles, 5, 0, 1, "\x00\x11\x01", preambles, 5, 7) + 'A'*240
			hart_packet = hart_protocol.get_packet(0x06, payload[1], preambles, ord(payload[2]), 0, 208, newpacket, 0)
			print hart_protocol.dump_hex(hart_packet)
			ser.write(hart_packet)
		else:
			# unknown command
			pass
			
	time.sleep(0.001) 