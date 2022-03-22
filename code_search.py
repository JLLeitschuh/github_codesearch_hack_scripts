import json
from dataclasses import dataclass
import urllib.parse

import requests
import yaml
from requests.exceptions import SSLError

from typing import Dict, Callable


@dataclass
class GitHubCodeSearchSite:
    host_blackbird: str
    login_state: str

    def _cookies(self) -> Dict:
        return {
            '__Host-blackbird': self.host_blackbird,
            'login_state': self.login_state
        }

    def _make_cs_get(self, url: str) -> Dict:
        r = GitHubCodeSearchSite._resilient_request(lambda: requests.get(
            url,
            cookies=self._cookies(),
        ))
        return r.json()

    def make_cs_search(self, search: str, page: int = 0) -> Dict:
        search_encoded = urllib.parse.quote(search)
        url = f'https://cs.github.com/api/search?q={search_encoded}&p={page}'
        return self._make_cs_get(url)

    def make_cs_search_json(self, search: str, page: int = 0) -> str:
        return json.dumps(self.make_cs_search(search, page), indent=2)

    @staticmethod
    def _resilient_request(request_method: Callable[[], requests.Response], retry_count: int = 0):
        try:
            return request_method()
        except SSLError as e:
            if retry_count < 4:
                return GitHubCodeSearchSite._resilient_request(request_method, retry_count + 1)
            raise Exception(f'SSL Error') from e

    @staticmethod
    def create_from_file() -> 'GitHubCodeSearchSite':
        with open('config.yml') as config_file:
            config = yaml.safe_load(config_file)
            github_cs = config['github_cs']
            return GitHubCodeSearchSite(
                github_cs['host_blackbird'],
                github_cs['login_state']
            )


if __name__ == '__main__':
    import sys

    github_cs = GitHubCodeSearchSite.create_from_file()
    print(github_cs.make_cs_search_json(' '.join(sys.argv[1:])))
