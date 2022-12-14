import difflib
import re
from typing import List, Iterable

import requests

from config import IGNORE_FOLDER


class Repository:
    path: str
    default_branch: str


class File:
    path: str
    content: str


class AntiPlagiarism:
    def __init__(self, token):
        self.auth_token = token

    def get_raw(self, urls: Iterable[str]) -> List[str]:

        res = []
        for url in urls:
            url = url.replace("/blob", "").replace("//github", "//raw.githubusercontent")
            r = requests.get(url, headers={"Authorization": f"Bearer {self.auth_token}"})
            res.append(r.text)

        return res

    def get_repo_files(self, repo: Repository, extension_regex: str = r'^.*\.(c|h|cpp)$') -> List[File]:

        r = requests.get(f"https://api.github.com/repos/{repo.path}/git/trees/{repo.default_branch}?recursive=1",
                         headers={"Authorization": f"Bearer {self.auth_token}"}).json()

        res = []
        for file in r['tree']:

            if any([ign in file['path'] for ign in IGNORE_FOLDER]) or file['mode'] == '040000':
                continue

            f = File()
            f.path = file['path']

            if re.search(extension_regex, f.path):
                url = f'https://raw.githubusercontent.com/{repo.path}/{repo.default_branch}/{file["path"]}'
                f.content = self.get_raw((url,))[0]
                res.append(f)

        return res

    def get_user_repos(self, user, language: str = 'c') -> list[Repository] | None:

        r = requests.get(f"https://api.github.com/users/{user}/repos",
                         headers={"Authorization": f"Bearer {self.auth_token}"}).json()

        if isinstance(r, dict):
            print("[!] Bad user", user)
            return

        res = []
        for repo in r:
            resp = Repository()
            if repo['language']:
                if language in repo['language'].lower() and not repo['fork']:
                    resp.path = repo['full_name']
                    resp.default_branch = repo['default_branch']
                    res.append(resp)

        return res

    def get_repo(self, path: str) -> Repository | None:

        r = requests.get(f"https://api.github.com/repos/{path}",
                         headers={"Authorization": f"Bearer {self.auth_token}"}).json()

        res = Repository()
        res.path = path

        try:
            res.default_branch = r['default_branch']
        except KeyError:
            print("[!] Bad repo", path)
            return

        return res


def comp_diff(source1: str, source2: str) -> float:
    diff = difflib.SequenceMatcher(None, source1, source2)
    return diff.ratio()
