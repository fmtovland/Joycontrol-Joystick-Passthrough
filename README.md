# How we got here
So I found a cool project on github which lets your computer emulate a switch controller. Check it out at https://github.com/mart1nro/joycontrol It's a dependency anyway. And was like, "I could totally pass a controller through to my switch from my desktop while logging the inputs in another program altogether. A few hours of coding later and here we are.

# Getting up and running
Your first question might be "Why the hell is this client server?". The answer was that I was running the server with a VM so that I could still use other bluetooth devices at the same time without worrying about messing up my environment. You know, since it involves modifying the bluetooth systemd service. I suppose you could run them off the same machine, but I'm not going to do that.

# server
Download and install the original person's code and run the cli script to pair your switch. I'd recommend running it in a debian VM. Make the required changes to the systemd service of bluetooth. to start the server type python3 server.py $SWITCH_BT_MAC_ADDRESS.

# client
Install inputs from pip. Run configure.py. I have nothing but contempt for the sort of imbiciles who make programs with non remappable buttons, so I made the effort. It's not perfect, almost on par with your average emulator, mind the lack of deadzones. It will create a file mapping your controller's buttons to buttons on a switch pro controller, and output a json file. Once you've got that, run client.py with the hostname of the computer where the server is running.

# Notes
Neither the client nor server give any useful error messages besides throwing exceptions. I appologise. With that said, have fun with whatever you wind up doing with the code. Peace.
