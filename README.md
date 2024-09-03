# hugomanage

A TUI tool for managing Hugo blog posts easily. 

## Usage
```
hugomanage create           Create a new Hugo blog post in a new Git branch
hugomanage sync             Merge all new posts into the master branch, discarding any other changes 
hugomanage discard          Delete a given blog post     
hugomanage abort            Discard all changes and revert to the main branch
```

If there is a file present in the CWD called `example.md`, it will be used as a template for the frontmatter fields when creating a new post.


