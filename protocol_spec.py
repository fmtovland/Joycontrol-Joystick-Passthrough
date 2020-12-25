version=2
import enum

class Instruction(enum.IntEnum):
	version_check=0
	set_button=1
	set_axis=2

class Axis(enum.IntFlag):
	h=1
	v=2
	lstick=4
	rstick=8

class Axis1(enum.IntEnum):
	lstick_h=Axis.lstick|Axis.h
	lstick_v=Axis.lstick|Axis.v
	rstick_h=Axis.rstick|Axis.h
	rstick_v=Axis.rstick|Axis.v

Button=enum.IntEnum('Button',names=['y', 'x', 'b', 'a', 'zr', 'r',
'minus', 'plus', 'r_stick', 'l_stick', 'home', 'capture',
'down', 'up', 'right', 'left', 'zl', 'l'])

_Axis1={a.name:a for a in Axis1}
_Button={b.name:b for b in Button}
