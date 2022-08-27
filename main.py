from RequestFunctions import RequestGet, SetTokenAPI

GithubAPIToken = ""
with open("E:\\GithubProjects\\githubapitoken.txt", "r", encoding="utf-8") as f:
	GithubAPIToken = f.readline()
	SetTokenAPI(GithubAPIToken)

GithubUser = "kysth0707"
# GithubUser = "banksemi"

GithubRepos = RequestGet(f"https://api.github.com/users/{GithubUser}/repos")

for i in range(len(GithubRepos)):
	RepoName = GithubRepos[i]['name']
	IsFork = GithubRepos[i]['fork']

	Commits = RequestGet(f"https://api.github.com/repos/{GithubUser}/{RepoName}/commits")
	try:
		LastCommit = Commits[0]['commit']['author']['date']
	except:
		LastCommit = "?"

	print(f"{RepoName} / fork : {IsFork} / LastCommit = {LastCommit}")

print("\n")
UserData = RequestGet(f"https://api.github.com/users/{GithubUser}")
print(f"ID : {UserData['login']}")
print(f"생성 날짜 : {UserData['created_at']}")
print(f"리포지토리 개수 : {UserData['public_repos']}")