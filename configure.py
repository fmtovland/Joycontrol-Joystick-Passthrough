from inputs import get_gamepad
from protocol_spec import Button, Axis1
from time import sleep

import json

button_map={}
axis_map={}
axisable_buttons=[Button.zr,Button.zl,Button.up,Button.down,Button.left,Button.right]

for button in Button:
	print('enter button for',button,'or press ctrl-c to skip')
	while button.name not in button_map.values():
		try:
			for event in get_gamepad():
				if event.ev_type == 'Absolute':
					if button not in axisable_buttons:
						continue
					event.code+='+' if event.state>0 else '-'

				if event.ev_type not in ['Absolute','Key']:
					continue
				elif event.state == 0:
					continue
				elif event.code in button_map:
					continue
				else:
					button_map[event.code]=button.name
					print(event.code)
					break

		except KeyboardInterrupt:
			break
	sleep(.1)

for axis in Axis1:
	for event in get_gamepad():
		pass
	sleep(2)
	print('enter axis for',axis,'or press ctrl-c to skip')
	while axis.name not in axis_map.values():
		try:
			for event in get_gamepad():
				if event.ev_type != 'Absolute':
					continue
				if event.code in axis_map:
					continue
				else:
					axis_map[event.code]=axis.name
					print(event.code)
					break

		except KeyboardInterrupt:
			break

with open('button_map.json',"w+") as output_file:
	output_file.write(json.dumps({'button_map':button_map,'axis_map':axis_map}))
