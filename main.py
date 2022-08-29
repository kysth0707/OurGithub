from RequestFunctions import RequestGet, SetTokenAPI, RequestImageGet
import os

def ReturnPos(loc : str):
	return os.getcwd() + loc

GithubAPIToken = ""
with open("E:\\GithubProjects\\githubapitoken.txt", "r", encoding="utf-8") as f:
	GithubAPIToken = f.readline()
	SetTokenAPI(GithubAPIToken)

GithubUser = "kysth0707"
# GithubUser = "banksemi"



GithubRepos = RequestGet(f"https://api.github.com/users/{GithubUser}/repos")

f = open(ReturnPos(f"\\Data.txt"), "w", encoding="utf-8")

for i in range(len(GithubRepos)):
	RepoName = GithubRepos[i]['name']
	IsFork = GithubRepos[i]['fork']
	StarCount = GithubRepos[i]['stargazers_count']

	Commits = RequestGet(f"https://api.github.com/repos/{GithubUser}/{RepoName}/commits")
	try:
		LastCommit = Commits[0]['commit']['author']['date']
	except:
		LastCommit = "?"

	if IsFork == False:
		f.write(f"{GithubUser},{RepoName},{StarCount},{LastCommit}\n")

f.close()

print("\n")
UserData = RequestGet(f"https://api.github.com/users/{GithubUser}")
print(f"ID : {UserData['login']}")
print(f"생성 날짜 : {UserData['created_at']}")
print(f"리포지토리 개수 : {UserData['public_repos']}")
RequestImageGet(UserData['avatar_url'], ReturnPos(f"\\imgs\\profiles\\MyProfile.png"))

FollowerData = RequestGet(f"https://api.github.com/users/{GithubUser}/followers")
for i in range(3):
	try:
		RequestImageGet(FollowerData[i]['avatar_url'], ReturnPos(f"\\imgs\\profiles\\Followers-{FollowerData[i]['login']}.png"))
	except:
		pass
# avatar_url
# followers_url