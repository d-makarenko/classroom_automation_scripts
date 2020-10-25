#!/usr/bin/python
from appveyor_client import AppveyorClient as AC
from classroom_automation_tokens import APPVEYOR_TOKEN
from datetime import datetime
client = AC(APPVEYOR_TOKEN)
appveyor_projects = client.projects.get()

for project in appveyor_projects:
    created = datetime.strptime(project['created'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
    days_since_created = (datetime.today() - created).days
    if days_since_created > 365//2:
        print(f"Removing project: {project['name']}")
        client.projects.delete('d-makarenko', project['slug'])

