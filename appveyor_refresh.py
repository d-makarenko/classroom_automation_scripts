#!/usr/bin/python
from appveyor_client import AppveyorClient as AC
from classroom_automation_tokens import APPVEYOR_TOKEN, GITHUB_TOKEN
from github import Github

client = AC(APPVEYOR_TOKEN)
appveyor_projects = client.projects.get()

gh = Github(GITHUB_TOKEN)

miee = gh.get_organization("MIEE-ACS")

repos = gh.search_repositories(query='org:MIEE-ACS is:public created:>2020-08-01 zadanie')

repos_names = [r.name for r in repos]
appveyor_existing_projects = [ x["name"] for x in appveyor_projects ]

newrepos = [x for x in repos_names if x not in appveyor_existing_projects]

for x in newrepos:
    print(f"adding {x} repo")
    client.projects.add("gitHub", "MIEE-ACS/"+x)

