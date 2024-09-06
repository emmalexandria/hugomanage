import frontmatter
import os
import sys
import inquirer
import argparse
import git

from files import HugomanageInfo, merge_changes 

def main(): 
    parser = argparse.ArgumentParser(prog="hugomanage", description="Integrates with git branching to manage Hugo content files")
    subparsers = parser.add_subparsers(title="subcommands")

    create_parser = subparsers.add_parser('create')
    create_parser.set_defaults(func=create_file)

    sync_parser = subparsers.add_parser('sync')
    sync_parser.set_defaults(func=sync_changes)

    remove_parser = subparsers.add_parser('discard')
    remove_parser.set_defaults(func=discard_changes)

    remove_parser = subparsers.add_parser('remove')
    remove_parser.set_defaults(func=remove_file)
    
    
    args = parser.parse_args()
    args.func()
    

def create_file():
    repo = git.Repo('./')
    info = HugomanageInfo()

    content_types = (get_content_dirs() or [])
    if len(content_types) == 0:
        sys.stderr.write("No Hugo content directory found")
        return

    content_type = content_types[0]
    if len(content_types) > 1:
        content_type = get_content_type(content_types)

    example_post = get_example_frontmatter(content_type)
    if example_post == None:
        sys.stderr.write("No example frontmatter for the selected content type")
        return

    example_post.content = ""

    output_text = frontmatter.dumps(example_post)

    filename = get_filename()
    path = content_type + "/" + filename

    while os.path.exists(path) and os.path.isdir(path) != True:
        print("File already exists, please enter another name")
        filename = get_filename()
        path = content_type + "/" + filename

    frontmatter_str = frontmatter.dumps(example_post)
    output_file = open(path, "w+")
    output_file.write(frontmatter_str)

def sync_changes():
    info = HugomanageInfo()
    repo = git.Repo('./')

    merge_changes(info, repo)
    

def discard_changes():
    return

def remove_file():
    return
    
       
def get_filename():
    prompt_result = (inquirer.prompt([inquirer.Text('filename', message="Enter filename")]) or {"filename": "unknown"})
    return prompt_result['filename']



def get_content_type(content_types):
    types = [inquirer.List('type', message="What type of content would you like to create?", choices=content_types)]
    c_type = (inquirer.prompt(types) or {"type": "content"})
    return c_type["type"]

def get_example_frontmatter(dir):
    path = dir + "/frontmatter.txt"
    if os.path.exists(path) != True:
        return None

    return frontmatter.load(dir + "/frontmatter.txt")

def get_content_dirs():
    if os.path.isdir('content') != True:
        return 
    subdirs = [ f.path for f in os.scandir('content') if f.is_dir() ]

    valid_subdirs = []
    for dir in subdirs:
        for file in os.listdir(dir):
            if file == "frontmatter.txt":
                valid_subdirs.append(dir)

    return valid_subdirs 

if __name__ == "__main__":
    main()
