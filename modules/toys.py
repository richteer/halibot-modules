from module import XMPPModule
from subprocess import check_output as px

def get_fortune():
	try:
		out = px("fortune",universal_newlines=True)
	except:
		return None
	return out

def get_pom():
	try:
		out = px("pom",universal_newlines=True)
	except:
		return None
	return out

def handle_fortune(string):
	return get_fortune()

def handle_pom(string):
	return get_pom()

def handle_cowsay(string):
	if string == None:
		return None

	if string == "!fortune":
		string = get_fortune()
		if string == None:
			return None
	if string == "!pom":
		string = get_pom()
		if string == None:
			return None

	try:
		out = px(["cowsay"] + string.split(" "),universal_newlines=True)
	except:
		return None

	return '\n' + out


class Toys(XMPPModule):
	def help(self, feature):
		if feature in ['cowsay', '!cowsay']:
			return '''
A cowfigurable cow to play with.

usage: !cowsay [arguments to cowsay]
usage: !cowsay <!fortune|!pom>
'''
		if feature in ['fortune', '!fortune']:
			return '''
Forsees the future.

usage: !fortune
'''
		if feature in ['pom', '!pom']:
			return '''
The current phase of the moon.

usage: !pom
'''
		return '''
A modules to provides some nice toys to play with.

Module features:
 cowsay  - A configurable cow to play with.
 fortune - Forsees the future.
 pom     - The current phase of the moon.
'''

	def handleMessage(self, msg):
		command, string = (msg['body'].split(" ")[0]," ".join(msg['body'].split(' ')[1:]))
		if command in commands.keys():
			self.xmpp.reply(msg,commands[command](string))

commands = {
	"!cowsay":handle_cowsay,
	"!fortune":handle_fortune,
	"!pom":handle_pom
}
