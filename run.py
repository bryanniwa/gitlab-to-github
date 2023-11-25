import json
import os
import tempfile

from lib.github import GitHub
from lib.gitlab import GitLab

details = json.load(open("details.json"))

gitlab = GitLab(details["gitlab"]["url"], details["gitlab"]["token"])
github = GitHub(details["github"]["url"], details["github"]["token"])

projects = gitlab.get_all_projects()

for project in projects:
    new_url = github.create_repository(project["name"], project["description"])
    if not new_url:
        continue

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        os.system(f"git clone {project['sshUrlToRepo']} {project['path']}")
        os.chdir(f"{temp_dir}/{project['path']}")
        os.system(f"git remote add github {new_url}")
        os.system("git push --mirror github")
