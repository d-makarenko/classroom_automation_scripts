#!/usr/bin/python
from appveyor_client.appveyor_client import AppveyorClient as AC
from classroom_automation_tokens import APPVEYOR_TOKEN
from datetime import datetime
client = AC(APPVEYOR_TOKEN)

project_pages = client.projects.get_pages_count('d-makarenko')

for page in reversed(range(project_pages)):
    appveyor_projects = client.projects.get_page('d-makarenko', page)

    for project in appveyor_projects:
        created = datetime.strptime(project['created'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        days_since_created = (datetime.today() - created).days
        if days_since_created > 365//2:
            print(f"Removing project: {project['name']}")
            client.projects.delete('d-makarenko', project['slug'])

