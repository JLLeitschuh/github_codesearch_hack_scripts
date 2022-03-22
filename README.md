# GitHub Code Search Hack Scripts

A collection of scripts to make working with GitHub Code Search ([cs.github.com](https://cs.github.com)) easier.

## How

Unfortunately, because this solution isn't officially supported, there are a few pieces of API information you'll
need to extract manually while interacting with the [cs.github.com](https://cs.github.com) site.

### Using this Project

In order to extract these 'keys' for uses by these scripts, we recommend that your browser's develper tools
and inspect the various requests normally made under the 'Network' tab. This information should be put inside of a
file named `config.yml` inside the repositories root directory. This `config.yml` file is already part of the
`.gitignore` so adding it to this repository will not risk you accidentally committing it.

The format of this `config.yml` is the following:

```yaml
github_cs:
    host_blackbird: # From the request cookie `__Host-blackbird`
    login_state:    # From the request cookie `login_state`
```

## Usage Example

Search for Gradle Build Files that are using `http://` (instead of `https://`) for their `url` in the `repositories` block:

```shell
python code_search.py '(" url \"http://" OR "uri(\"http://" OR " url = uri(\"http://") AND ("maven {" OR "maven()" OR "ivy {" OR "ivy()") AND (path:*.gradle OR path:*.gradle.kts)' | jq '.results[] | { repo: .repo_name, path: .path }'
```
