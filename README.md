# hugomanage

A TUI tool for managing Hugo blog posts easily. 

## Usage

### Basics

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

### Non-technical users

To use `hugomanage`, you will need Python installed on your computer. Once installed, you may install `hugomanage` with `pip` by running `pip install hugomanage`. Once installed, navigate to the base directory of the Hugo project in the terminal.

To create a new file, run `hugomanage create`. Once created, the file will open in your default text editor. Edit it and then save it, running `hugomanage sync` to create a new Git branch and commit the files to it. `hugomanage discard` can be used to delete all files that have been created since the last `sync`, and `hugomanage remove` can be used to delete a single one.


