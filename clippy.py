#!/usr/bin/env python
import eventlet as eventlib
eventlib.monkey_patch()
import clips

namespace = "/"
 
def AddSpecificFunction(e, func, funcname=None):
	e.define_function(func, funcname)

class TempAns:
	def clearAns(self):
		self.temp_ans = None

	def __init__(self):
		self.temp_ans = self.clearAns()

	def setAns(self, ans):
		self.temp_ans = ans

	def getAns(self):
		return self.temp_ans

	def hasAns(self):
		return self.temp_ans != None

class Clippy:
	def __init__(self, socket, sid, source):
		clipsEnv = clips.Environment()
		AddSpecificFunction(clipsEnv, self.clips_debug, "debug")
		AddSpecificFunction(clipsEnv, self.clips_alert, "alert")
		AddSpecificFunction(clipsEnv, self.clips_prompt, "prompt")
		AddSpecificFunction(clipsEnv, self.clips_prompt2, "prompt2")
		AddSpecificFunction(clipsEnv, self.clips_final, "final")
		clipsEnv.load("{}.clp".format(source))
		self.ta = TempAns()
		self.socket = socket
		self.sid = sid
		self.clips = clips
		self.clipsEnv = clipsEnv
		self.final = []

	def clips_debug(self, message):
		print(message)
		self.socket.emit('debug', {'data': message}, namespace=namespace, room=self.sid)
		eventlib.sleep(.01)

	def clips_alert(self, message):
		print(message)
		self.socket.emit('alert', {'data': message}, namespace=namespace, room=self.sid)
		eventlib.sleep(.01)

	def clips_prompt(self, message, *options):
		print(message)
		print(options)
		self.socket.emit('prompt', {'data': message, 'options': [str(i) for i in options]}, namespace=namespace, room=self.sid)
		self.ta.clearAns()
		while not self.ta.hasAns():
			eventlib.sleep(1)
		user_input = self.ta.getAns()
		try:
			int(user_input)
			return self.clips.Integer(user_input)
		except:
			return self.clips.Symbol(user_input)

	def clips_prompt2(self, message, display, *options):
		print(message)
		zipped = zip([str(i) for i in options], display.split("\n"))
		print(zipped)
		self.socket.emit('prompt2', {'data': message, 'options': zipped}, namespace=namespace, room=self.sid)
		self.ta.clearAns()
		while not self.ta.hasAns():
			eventlib.sleep(1)
		user_input = self.ta.getAns()
		try:
			int(user_input)
			return self.clips.Integer(user_input)
		except:
			return self.clips.Symbol(user_input)

	def clips_final(self, message):
		print(message)
		self.socket.emit('debug', {'data': message}, namespace=namespace, room=self.sid)
		self.final.append(message)

	def run(self):
		eventlib.sleep(.01) # necessary with eventlet or first question won't appear (too soon after connect)
		self.clipsEnv.reset()
		self.clipsEnv.run()
		return self.final

	def setAns(self, ans):
		self.ta.setAns(ans)
