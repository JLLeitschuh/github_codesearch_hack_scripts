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

    def make_cs_search_page(self, search: str, page: int = 1) -> Dict:
        search_encoded = urllib.parse.quote(search)
        url = f'https://cs.github.com/api/search?q={search_encoded}&p={page}'
        return self._make_cs_get(url)

    def make_cs_search_json_page(self, search: str, page: int = 1) -> str:
        return json.dumps(self.make_cs_search_page(search, page), indent=2)

    def make_cs_search_merge_page_results(self, search: str) -> Dict:
        first_page_result = self.make_cs_search_page(search)
        if first_page_result['total_pages'] <= 1:
            return first_page_result['results']
        results = first_page_result['results'].copy()
        total_pages = first_page_result['total_pages']
        for page_number in range(1, total_pages):
            page_result = self.make_cs_search_page(search, page_number)
            results.extend(page_result['results'])
        return {'results': results}

    def make_cs_search_merge_page_results_json(self, search: str) -> str:
        return json.dumps(self.make_cs_search_merge_page_results(search), indent=2)

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
    import argparse

    parser = argparse.ArgumentParser('Query cs.github.com')
    parser.add_argument('query', help='Query string', type=str)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--page', metavar='P', help='Page number', type=int, default=0)
    group.add_argument(
        '--all-pages',
        help='Run query merging results from all paginated pages into one result',
        action='store_true'
    )

    args = parser.parse_args()

    github_cs = GitHubCodeSearchSite.create_from_file()
    if not args.all_pages:
        print(github_cs.make_cs_search_json_page(args.query, args.page))
    else:
        print(github_cs.make_cs_search_merge_page_results_json(args.query))
