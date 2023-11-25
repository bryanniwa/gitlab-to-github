import requests


class GitHub:
    def __init__(self, url: str, access_token: str):
        self.url = url
        self.access_token = access_token
        self.headers = {
            "Authorization": "Bearer " + access_token,
        }

    def _get_body(self, name, description) -> str:
        escaped_description = description.replace('"', '\\"') if description else ""
        return f"""
        mutation CreateRepository {{
            createRepository(input: {{name: "{name}", visibility: PRIVATE, description: "{escaped_description}"}}) {{
                clientMutationId
                repository {{
                    sshUrl
                }}
            }}
        }}
        """

    def create_repository(self, name: str, description: str = "") -> str:
        body = self._get_body(name, description)
        response = requests.post(
            url=self.url, headers=self.headers, json={"query": body}
        )

        if "errors" in response.json():
            msg = response.json()["errors"][0]["message"]
            if "Name already exists" in msg:
                new_name = input(
                    f"Repository {name} already exists. Enter a new name or press enter to skip: "
                )
                if not new_name:
                    return None
                else:
                    return self.create_repository(new_name, description)
            else:
                raise Exception(msg)

        return response.json()["data"]["createRepository"]["repository"]["sshUrl"]
