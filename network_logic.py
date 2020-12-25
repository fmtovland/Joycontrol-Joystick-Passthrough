import struct

from protocol_spec import *
from joycontrol.controller_state import button_push, button_press, button_release

class VersionError(Exception):
	pass

def null_function(*args):
	pass

def set_axis(controller_state,args):
	axis,value=args
	stick=controller_state.r_stick_state if axis&Axis.rstick else controller_state.l_stick_state

	if axis&Axis.h:
		stick.set_h(value)
	elif axis&Axis.v:
		stick.set_v(value)

def version_check(args):
	v=struct.unpack('!H',args)[0]
	print(v,version)
	if(v!=version):
		raise VersionError
	return null_function,None,False

def set_button_(args):
	button,value=struct.unpack('!BH',args)
	button=Button(button).name
	if value == 0:
		return button_release,(button),True
	else:
		return button_press,(button),True

def set_axis_(args):
	return set_axis,struct.unpack('!BH',args),False

handlers={
	Instruction.version_check:version_check,
	Instruction.set_button:set_button_,
	Instruction.set_axis:set_axis_,
}
