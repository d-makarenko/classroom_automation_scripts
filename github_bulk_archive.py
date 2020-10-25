from github import Github
from classroom_automation_tokens import GITHUB_TOKEN

g = Github(GITHUB_TOKEN)

for repo in g.get_user().get_repos():
    if repo.name.startswith("domashnee-zadanie"):
        if not repo.archived:
            try:
                repo.edit(archived=True)
                print(f"Archiving: {repo.name}")
            except:
                print(f"Failed to archive {repo.name}")
        if not repo.private:
            print(repo.name)
            try:
                repo.edit(private=True)
                print(f"Making private: {repo.name}")
            except Exception as e:
                print(f"Failed to make private: {repo.name}")
                print(e)
