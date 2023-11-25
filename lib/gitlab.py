import requests


class GitLab:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        }

    def get_singular_project(self, project_id: str):
        body = f"""
        query {{
            projects(ids: "{project_id}") {{
                nodes {{
                    name
                    id
                    description
                    path
                    sshUrlToRepo
                }}
            }}
        }}
        """
        response = requests.post(
            url=self.url, headers=self.headers, json={"query": body}
        )
        return response.json()["data"]["projects"]["nodes"][0]

    def get_all_projects(self):
        body = """
        query {
            projects(membership: true) {
                nodes {
                    name
                    id
                    description
                    path
                    sshUrlToRepo
                }
            }
        }
        """
        response = requests.post(
            url=self.url, headers=self.headers, json={"query": body}
        )
        return response.json()["data"]["projects"]["nodes"]
