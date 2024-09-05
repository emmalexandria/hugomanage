import frontmatter
import os
import sys
import inquirer

def main(): 
    content_types = (get_content_dirs() or [])
    if len(content_types) == 0:
        sys.stderr.write("No Hugo content directory found")
        return

    content_type = content_types[0]
    if len(content_types) > 1:
        content_type = get_content_type(content_types)

    frontmatter = get_example_frontmatter(content_type)
    if frontmatter == None:
        sys.stderr.write("No example frontmatter for the selected content type")
        return

    print("Please fill out the following frontmatter fields:")
    fields = []
    for key in frontmatter.metadata:
        fields.append(
            inquirer.Text(key, message="Enter a value for " + key)
        )

    inquirer.prompt(fields)
   


def get_content_type(content_types):
    types = [inquirer.List('type', message="What type of content would you like to create?", choices=content_types)]
    c_type = (inquirer.prompt(types) or {"type": "content"})
    return c_type["type"]

def get_example_frontmatter(dir):
    path = dir + "/frontmatter.md"
    if os.path.exists(path) != True:
        return None

    return frontmatter.load(dir + "/frontmatter.md")

def get_content_dirs():
    if os.path.isdir('content') != True:
        return 
    subdirs = [ f.path for f in os.scandir('content') if f.is_dir() ]
    subdirs.append('content')

    return subdirs

if __name__ == "__main__":
    main()
