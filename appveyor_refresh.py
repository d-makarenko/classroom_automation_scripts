#!/usr/bin/python
from appveyor_client.appveyor_client import AppveyorClient as AC
from classroom_automation_tokens import APPVEYOR_TOKEN, GITHUB_TOKEN
from github import Github

client = AC(APPVEYOR_TOKEN)

appveyor_existing_projects = [ x["name"] 
                               for page in reversed(range(client.projects.get_pages_count('d-makarenko'))) 
                               for x in client.projects.get_page('d-makarenko', page)]

gh = Github(GITHUB_TOKEN)

miee = gh.get_organization("MIEE-ACS")

repos = gh.search_repositories(query='org:MIEE-ACS is:public created:>2020-10-15 zadanie')

repos_names = [r.name for r in repos]



newrepos = [x for x in repos_names if x not in appveyor_existing_projects]

for x in newrepos:
    print(f"adding {x} repo")
    client.projects.add("gitHub", "MIEE-ACS/"+x)

