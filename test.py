from ModuleRequestFunc import RequestGet, SetTokenAPI

GithubAPIToken = ""
with open("E:\\GithubProjects\\githubapitoken.txt", "r", encoding="utf-8") as f:
	GithubAPIToken = f.readline()
	SetTokenAPI(GithubAPIToken)

GithubUser = "kysth0707"

Commits = RequestGet(f"https://api.github.com/repos/{GithubUser}/41x41display/commits")

print(Commits[0]['commit']['author']['date']) # 가장 최근꺼임

# Branch test