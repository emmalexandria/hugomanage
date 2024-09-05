import frontmatter
import os
import sys

def main(): 
    post = frontmatter.load("frontmatter.md")

    for key in post.metadata:
        print(key)

    content_types = get_content_dirs()
    if content_types == None:
        sys.stderr.write("No Hugo content directory found")

def get_content_dirs():
    if os.path.isdir('content') != True:
        return 
    subdirs = [ f.path for f in os.scandir('content') if f.is_dir() ]

    return subdirs

if __name__ == "__main__":
    main()
