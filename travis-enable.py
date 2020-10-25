#!/usr/bin/python
from travispy import TravisPy
from classroom_automation_tokens import TRAVIS_GITHUB_TOKEN
PATTERN= 'zadanie-noNUM-'
uri="https://api.travis-ci.com"

travis = TravisPy.github_auth(TRAVIS_GITHUB_TOKEN, uri=uri)

travis.user().sync()

for x in range(1, 7):
	for repo in travis.repos(search=PATTERN.replace("NUM", str(x)), active=False, limit=100):
		if not repo.active:
			repo.enable()


