import socket,struct,json
from protocol_spec import *
from protocol_spec import _Button,_Axis1
from sys import argv
from inputs import get_gamepad

with open("button_map.json") as config:
	a=json.loads(config.read())
	axis_map=a["axis_map"]
	button_map=a["button_map"]

axis_map={key:_Axis1[axis_map[key]] for key in axis_map}
button_map={key:_Button[button_map[key]] for key in button_map}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((argv[1],42069 if len(argv)<3 else int(argv[2])))
version_check=struct.pack('!BH',Instruction.version_check, version)
sock.send(version_check)
response=sock.recv(1)[0]
if response==0:
	print("Successful connection")
else:
	print("Server reported error")
try:
	while response==0:
		messages=[]
		for event in get_gamepad():
			if event.ev_type not in ('Absolute','Key'):
				continue

			obutton=None
			pbutton=button_map.get(event.code+'+')
			event_code_button=event.code+('+' if event.state>0 else '-')

			if event.code in axis_map:
				instruction=Instruction.set_axis
				button=axis_map[event.code]
				value=(event.state>>4)+2048
				if button & Axis.v:
					value=4095-value

			elif event_code_button in button_map:
				instruction=Instruction.set_button
				if event.state==0:
					button=button_map[event.code+'+']
					obutton=button_map[event.code+'-']
					sock.send(struct.pack('!BBH',instruction,button,0))
					sock.send(struct.pack('!BBH',instruction,obutton,0))
					continue
				elif pbutton in (Button.zr, Button.zl):
					button=pbutton
					value=event.state>150
				else:
					button=button_map[event_code_button]
					value=1

			elif event.code in button_map:
				instruction=Instruction.set_button
				button=button_map[event.code]
				value=event.state
			else:
				continue

			data=struct.pack('!BBH',instruction,button,value)
			sock.send(data)
finally:
	sock.close()
