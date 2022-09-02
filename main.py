import ModuleGUI

GUI = ModuleGUI.OutGithubGUI()
GUI.NoticeText = "공지 변경 테스트입니다."
GUI.MyID = "아이디 테스트입니다."
while True:
	GUI.Update()