import os
import datetime

def ReturnPos(loc : str):
	return os.getcwd() + loc

def GetDatas():
	f = open(ReturnPos(f"\\Datas\\Datas.txt"), "r", encoding="utf-8")
	Dates = []
	Datas = f.readlines()

	MyID = Datas[0][:-1]
	NoticeText = Datas[1][:-1].replace('{MyID}', MyID)

	return MyID, NoticeText

def LastCommitRefresh():
	f = open(ReturnPos(f"\\Datas\\MyRepo.txt"), "r", encoding="utf-8")
	Dates = []
	Datas = f.readlines()
	for i in range(len(Datas)):
		Val = Datas[i][:-1].split(',')
		try:
			Dates.append(datetime.datetime.strptime(Val[3], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=9))
		except:
			Dates.append(None)
	f.close()

	LastTime = None
	for i in range(len(Dates)):
		if Dates[i] != None:
			if LastTime == None:
				LastTime = Dates[i]
			elif Dates[i] > LastTime:
				LastTime = Dates[i]

	if LastTime == None:
		LastCommitDate = "X"
	else:
		LastCommitDate = LastTime
	return LastCommitDate


def ReturnLimitText(TextValue, Limit):
	if len(TextValue) > Limit + 1:
		TextValue = TextValue[:Limit]+"..."
	return TextValue

def SortWith(Value, Other, Other2):
	for x in range(len(Value)):
		for y in range(len(Value)):
			if Value[x] > Value[y]:
				Value[x], Value[y] = Value[y], Value[x]
				Other[x], Other[y] = Other[y], Other[x]
				Other2[x], Other2[y] = Other2[y], Other2[x]
	return Value, Other, Other2

def MyRepoRefresh():
	
	MyRepoName = []
	MyRepoStar = []
	MyRepoTime = []

	f = open(ReturnPos(f"\\Datas\\MyRepo.txt"), "r", encoding="utf-8")
	Datas = f.readlines()
	for i in range(len(Datas)):
		Val = Datas[i][:-1].split(',')
		MyRepoName.append(Val[1])
		MyRepoStar.append(int(Val[2]))
		MyRepoTime.append(Val[3])

	return SortWith(MyRepoStar, MyRepoName, MyRepoTime)