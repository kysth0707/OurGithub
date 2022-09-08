import ModuleGUI

import time
class Timer:
	lasttime = 0
	def __init__(self) -> None:
		self.lasttime = time.time()

	def Check(self):
		return time.time() - self.lasttime

	def Update(self):
		self.lasttime = time.time()


# MyTimer = Timer()

GUI = ModuleGUI.OutGithubGUI("kysth0707")
GUI.NoticeText = "공지 변경 테스트입니다."
while True:
	GUI.Update()
	# print(f"{1 / MyTimer.Check()} fps")
	# MyTimer.Update()