#!/usr/bin/env python3

# Usage
# =====
#
# Run `git-allow` (or `git allow`) to ensure that .gitallow is sorted
# and that .gitignore has a pattern that satisfies it.
#
# Use arguments, like `git-allow .vimrc`, to add files to .gitallow.

import subprocess
import os

import sys

git_top_level = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True
).stdout.rstrip().decode('utf8')

gitignore = os.path.join(git_top_level, '.gitignore')
gitallow = os.path.join(git_top_level, '.gitallow')

output = [
    "# Warning: File is generated from .gitallow, do not edit.",
    "# <https://github.com/christianbundy/dotfiles/blob/main/.local/bin/git-allow>",
    "/*",
]

default_allow_list = [
    ".gitallow",
    ".gitignore"
]

try:
    file = open(gitallow, 'r+')
    allow_list = [line.rstrip().strip('/')
                  for line in file] + default_allow_list
except FileNotFoundError:
    file = open(gitallow, 'w')
    allow_list = default_allow_list
finally:
    for allow_path in [path.strip('/') for path in sys.argv[1:]]:
        if allow_path not in output:
            allow_list.append(allow_path)

    allow_list = sorted(list(set(allow_list)))

    for item in allow_list:
        fragments = item.split("/")
        for index, _ in enumerate(fragments):
            fragment = "/" + "/".join(fragments[0:index + 1])
            allow = "!" + fragment
            deny = fragment + "/*"
            if allow not in output:
                output.append(allow)
                if index < len(fragments) - 1:
                    output.append(deny)

    file.seek(0)
    explicit_allow_list = [
        x for x in allow_list if x not in default_allow_list]
    file.write("\n".join(explicit_allow_list) + "\n")
    file.truncate()

with open(gitignore, 'w') as file:
    file.write("\n".join(output) + "\n")
