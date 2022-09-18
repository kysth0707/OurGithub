import ModuleGUI
import os


def ReturnPos(loc : str):
	return os.getcwd() + loc

try:
	with open(ReturnPos("\\Datas\\User.txt")) as f:
		User = f.readline()
		print(User)

	if User == "":
		from tkinter import messagebox
		messagebox.showwarning("사용자 아이디가 없습니다", "사용자 아이디를 지정해주세요.\n\n현재 폴더\\Datas\\User.txt 에서 변경이 가능합니다!\n변경 후, 재 실행 부탁드립니다.")
		exit()


except:
	exit()


GUI = ModuleGUI.OutGithubGUI(User)
while True:
	GUI.Update()