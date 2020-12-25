import asyncio,socket
from os import environ
from sys import argv

from network_logic import handlers,version_check

from joycontrol.controller import Controller
from joycontrol.controller_state import ControllerState
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

switch_bt_address=argv[1] if len(argv)>1 else None

async def handle_network(reader,writer):
	transport, protocol, controller_state=await(get_controller())

	#check version
	data=await reader.read(4)
	version_check(data[1:])
	writer.write((0).to_bytes(1,'big'))

	await controller_state.connect()
	try:
		while True:
			data=await reader.read(4)
			f,arg,isasync=handlers[data[0]](data[1:])
			if isasync:
				await f(controller_state,arg)
			else:
				f(controller_state,arg)
			#writer.write((0).to_bytes(1,'big'))
	except IndexError as e:
		print("empty packet recieved")
	finally:
		await transport.close()
		writer.write((1).to_bytes(1,'big'))
		print("connection closed")

async def get_controller():
	#setup controller
	spi_flash = FlashMemory()
	ctl_psm, itr_psm = 17, 19
	factory = controller_protocol_factory(Controller.PRO_CONTROLLER, spi_flash=spi_flash)
	transport, protocol = await create_hid_server(factory,
						reconnect_bt_addr=switch_bt_address,
						ctl_psm=ctl_psm,
						itr_psm=itr_psm,)
	controller_state = protocol.get_controller_state()
	return transport, protocol, controller_state

loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle_network,port=42069))
loop.run_forever()
