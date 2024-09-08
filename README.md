# hugomanage

A TUI tool for managing Hugo blog posts easily. 

## Usage
```
usage: hugomanage [-h] {create,sync,discard,remove} ...

Integrates with git branching to manage Hugo content files

options:
  -h, --help            show this help message and exit

subcommands:
  {create,sync,discard,remove}
    create              Create a new markdown file to be edited
    sync                Add the files to a new git branch and commit
    discard             Delete all added files
    remove              Delete a particular added file
```

`hugomanage` checks all subdirectories of the Hugo content directory for a file called `frontmatter.txt`. If found, this file will become the base for the frontmatter of files created with the tool. Added files will be pushed to a branch in the repository named after the file, and pushed to remote automatically.


