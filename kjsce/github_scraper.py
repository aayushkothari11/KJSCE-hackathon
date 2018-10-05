from github import Github, GithubException
from decouple import config
import base64

g = Github(config('GITHUB_USER'), config('GITHUB_PASS'))

def get_user_info(user_link):
	num_of_repos = 0
	repos = []
	followers = 0
	try:
		username = user_link.strip('/').split("/")[-1]
		user = g.get_user(username)
		for r in user.get_repos():
			temp = []
			temp.append(r.name)
			temp.append(r.language)
			try:
				temp.append(base64.b64decode(r.get_readme().content))
			except GithubException:
				temp.append('')
			repos.append(temp)
			num_of_repos += 1
		followers = user.followers
	except GithubException:
		print("No user found")
		return None
	return {"num_of_repos": num_of_repos, "repos": repos, "followers": followers}

# print(get_user_info('www.github.com/arsenal-2004'))
print(g.rate_limiting)

