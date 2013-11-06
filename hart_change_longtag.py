import serial,time,socket
import hart_protocol
import sys

port = 3

if len(sys.argv) < 4:
	print "Error, usage " + sys.argv[0] + " port long_address new_longtag"
	print "Usage hex string (5 hex digits) as address and LATIN-1 string as new long tag"
	quit()

address = sys.argv[2].decode('hex')

if len(address) != 5:
	print "Error, address should be 5 bytes long!"
	                                                                                           
longtag = sys.argv[3]

if len(longtag) != 32:
	print "Error, long tag should be 32 bytes long!"

port = int(sys.argv[1]) - 1

print "Opening COM" + str(port + 1) + "..."

preambles = 10

delimiter = '\x82' # master command with long address
command = '\x16' # write long tag 
ln = 32 # long address exact length
pack = delimiter + address + command + chr(ln) + longtag
packet = '\xff' * preambles + pack + hart_protocol.get_checksum(pack)

ser = serial.Serial(port, 1200)
print "writing: " + hart_protocol.dump_hex(packet)
ser.write(packet)
print "packet sent succesfully!"