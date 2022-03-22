from dataclasses import dataclass
import urllib.parse

import requests as requests
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

    def _make_cs_search(self, search: str, page: int = 0) -> Dict:
        search_encoded = urllib.parse.quote(search)
        url = f'https://cs.github.com/api/search?q={search_encoded}&p={page}'
        return self._make_cs_get(url)

    @staticmethod
    def _resilient_request(request_method: Callable[[], requests.Response], retry_count: int = 0):
        try:
            return request_method()
        except SSLError as e:
            if retry_count < 4:
                return GitHubCodeSearchSite._resilient_request(request_method, retry_count + 1)
            raise Exception(f'SSL Error') from e
