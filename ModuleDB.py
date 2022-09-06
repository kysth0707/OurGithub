import pymysql
import threading
import datetime
import ModuleRequest
import ModuleContributions

lock = threading.Lock()

f = open("C:/Users/th070/Desktop/mysql_test/password.txt", "r", encoding="utf-8")
pw = f.readline()
f.close()

MyDB = pymysql.connect(
	user='root', 
	passwd=pw,
	host='127.0.0.1', 
	db='outgithub', 
	charset='utf8'
)
cursor = MyDB.cursor(pymysql.cursors.DictCursor)


def Now():
	return datetime.datetime.now()

def Command(cmd):
	global MyDB
	with lock:
		cursor.execute(cmd) # 이렇게 작성하면 cmd 를 mysql 에서 실행시킨다는 얘기
		MyDB.commit()

def GetData(cmd):
	global cursor
	with lock:
		cursor.execute(cmd) # cmd 를 실행시키고 반환받은 값들을 리턴함
		
		result = cursor.fetchall()
	return result

def GetNumBy(Table, Row):
	Num = GetData(f"SELECT * FROM {Table} ORDER BY {Row} DESC LIMIT 1;")
	try:
		Num = Num[0]['Num'] + 1
	except:
		Num = 0

	return Num



def AddRepoLog(ID, RepoName, Star, LastCommit, CreateDate):
	Num = GetNumBy("repos", "Num")

	AlreadyExist = False

	try:
		GetData(f"SELECT * FROM repos WHERE ID = '{ID}' AND RepoName = '{RepoName}';")[0]
		AlreadyExist = True
	except:
		pass

	if LastCommit == "?":
		LastCommit = "0000-00-00T00:00:00Z"

	if AlreadyExist:
		Command(f"UPDATE repos SET Num = {Num}, ID = '{ID}', RepoName = '{RepoName}', Star = {Star}, LastCommit = '{LastCommit}', CreateDate = '{CreateDate}' WHERE ID = '{ID}' AND RepoName = '{RepoName}'")
	else:
		Command(f"INSERT INTO repos VALUES ({Num}, '{ID}', '{RepoName}', {Star}, '{LastCommit}', '{CreateDate}')")

	pass

def UpdateRepos(ID):
	Datas = ModuleRequest.GetRepoDatas(ID)
# 	Datas = [{'ID': 'kysth0707', 'RepoName': '2D-game', 'Star': 0, 'LastCommit': '?', 'CreatedAt': '2022-08-21T01:33:05Z'}, {'ID': 'kysth0707', 'RepoName': '2DGame', 'Star': 0, 'LastCommit': '?', 'CreatedAt': '2022-08-21T01:35:36Z'}, {'ID': 'kysth0707', 'RepoName': 'ChatPractice', 'Star': 0, 'LastCommit': '2022-05-06T09:51:05Z', 'CreatedAt': '2022-05-06T09:49:11Z'}, {'ID': 'kysth0707', 'RepoName': 'ColorIt', 'Star': 0, 'LastCommit': '2022-03-19T07:32:36Z', 'CreatedAt': '2022-03-19T07:02:38Z'}, {'ID': 'kysth0707', 'RepoName': 'GeekbleLang', 'Star': 2, 'LastCommit': '2022-04-22T08:34:34Z', 'CreatedAt': '2022-04-19T12:10:15Z'}, {'ID': 'kysth0707', 'RepoName': 'Light', 'Star': 0, 'LastCommit': '?', 'CreatedAt': '2022-06-19T02:51:54Z'}, {'ID': 'kysth0707', 'RepoName': 'LineMaker', 'Star': 2, 'LastCommit': '2022-08-28T04:29:39Z', 'CreatedAt': '2022-08-26T11:52:25Z'}, {'ID': 'kysth0707', 
# 'RepoName': 'Minecraft-Skripts', 'Star': 0, 'LastCommit': '2022-03-20T06:28:48Z', 'CreatedAt': '2022-03-20T06:26:10Z'}, {'ID': 'kysth0707', 'RepoName': 'MysqlHomepage', 'Star': 2, 'LastCommit': '2022-08-21T01:30:55Z', 'CreatedAt': '2022-08-20T10:39:55Z'}, {'ID': 'kysth0707', 'RepoName': 'OurGithub', 'Star': 1, 'LastCommit': '2022-09-02T08:10:23Z', 'CreatedAt': '2022-08-27T14:21:37Z'}]
	# print(Datas)
	for i in range(len(Datas)):
		AddRepoLog(Datas[i]['ID'], Datas[i]['RepoName'], Datas[i]['Star'], Datas[i]['LastCommit'], Datas[i]['CreatedAt'])
	pass

def AddUser(ID):
	Num = GetNumBy("users", "Num")

	try:
		GetData(f"SELECT * FROM users WHERE ID = '{ID}';")[0]
		return False
	except:
		pass
	
	Command(f"INSERT INTO users VALUES ({Num}, '{ID}', '{Now()}')")
	UpdateRepos(ID)
	return True

def UpdateContributions(ID):
	Value = ModuleContributions.Get(ID)
	# print(Value)

	Num = GetNumBy("contris", "Num")
	AlreadyExist = False

	try:
		GetData(f"SELECT * FROM contris WHERE ID = '{ID}';")[0]
		AlreadyExist = True
	except:
		pass

	SumValue = 0
	for i in range(7):
		SumValue += Value[i]

	if AlreadyExist:
		Command(f"UPDATE contris SET Monday = {Value[0]},  Tuesday = {Value[1]},  Wednesday = {Value[2]},  Thursday = {Value[3]},  Friday = {Value[4]},  Saturday = {Value[5]}, Sunday = {Value[6]}, Sum = {SumValue} WHERE ID = '{ID}'")
	else:
		Command(f"INSERT INTO contris VALUES ({Num}, '{ID}', {Value[0]}, {Value[1]}, {Value[2]}, {Value[3]}, {Value[4]}, {Value[5]}, {Value[6]}, {SumValue})")

	pass


def GetContributions(ID):
	Value = GetData(f"SELECT * FROM contris WHERE ID = '{ID}';")
	return Value
	# pass

def GetRepoDatas(ID):
	Value = GetData(f"SELECT * FROM repos WHERE ID = '{ID}';")
	# print(Value)
	if len(Value) != 0:
		return Value
	else:
		return False
	# pass

def GetTopStars():
	TopStars = GetData("SELECT * FROM repos ORDER BY Star DESC LIMIT 4;")
	return TopStars

def GetTopCommiters():
	TopCommiters = GetData("SELECT * FROM contris ORDER BY Sum DESC LIMIT 4;")
	return TopCommiters

def GetRecentCommits():
	RecentCommits = GetData("SELECT * FROM repos ORDER BY LastCommit DESC LIMIT 4;")
	return RecentCommits

def GetNewRepos():	
	NewRepos = GetData("SELECT * FROM repos ORDER BY CreateDate DESC LIMIT 4;")
	return NewRepos

# AddUser("kysth0707")
# UpdateContributions("kysth0707")

# GetContributions("kysth0707")
# GetRepoDatas("kysth0707")
