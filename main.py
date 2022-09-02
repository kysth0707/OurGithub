# import time
# from threading import Thread

# def GUIThread():
# 	import ModuleGUI

# temp = Thread(target=GUIThread)
# # temp.daemon = True
# temp.start()

# # Infinity Loop

import ModuleGUI

GUI = ModuleGUI.OutGithubGUI()
GUI.NoticeText = "공지 변경 테스트입니다."
GUI.MyID = "아이디 테스트입니다."
while True:
	GUI.Update()