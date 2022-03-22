# GitHub Code Search Hack Scripts

A collection of scripts to make working with GitHub Code Search ([cs.github.com](https://cs.github.com)) easier.

## Usage Example

Search for Gradle Build Files that are using `http://` for their `url` in the `repositories` block:
```shell
python code_search.py '(" url \"http://" OR "uri(\"http://" OR " url = uri(\"http://") AND ("maven {" OR "maven()" OR "ivy {" OR "ivy()") AND (path:*.gradle OR path:*.gradle.kts)' | jq '.results[] | { repo: .repo_name, path: .path }'
```
