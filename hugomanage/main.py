import frontmatter
import os
import sys
import inquirer
import argparse
import git

from files import HugomanageInfo, merge_changes, open_file_in_editor

def main(): 
    parser = argparse.ArgumentParser(prog="hugomanage", description="Integrates with git branching to manage Hugo content files")
    subparsers = parser.add_subparsers(title="subcommands")

    create_parser = subparsers.add_parser('create', help="Create a new markdown file to be edited")
    create_parser.set_defaults(func=create_file)
    create_parser.add_argument('-n', '--no_open', help="Don't open the created file in the system default text editor", action='store_true')

    sync_parser = subparsers.add_parser('sync', help="Add the files to a new git branch and commit")
    sync_parser.set_defaults(func=sync_changes)

    remove_parser = subparsers.add_parser('discard', help="Delete all added files")
    remove_parser.set_defaults(func=discard_changes)

    remove_parser = subparsers.add_parser('remove', help="Delete a particular added file")
    remove_parser.set_defaults(func=remove_file)
    
    
    args = parser.parse_args()
    

    func = None

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")

    func(args)
    

def create_file(args):
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

    info.file_names.append(path)
    info.save()
    print("Created file at " + path)


    if args.no_open != True:
        open_file_in_editor(path)


def sync_changes(args):
    info = HugomanageInfo()
    repo = git.Repo('./')

    merge_changes(info, repo)
    print("Files pushed to remote repository")

def discard_changes(args):
    info = HugomanageInfo()
    if len(info.file_names) == 0:
        print("No files to remove.")
        return

    filtered_files = filter_filenames(info)
    for f in filtered_files:
        info.file_names.remove(f)
        if os.path.exists(f):
            os.remove(f)

    info.save()

def remove_file(args):
    info = HugomanageInfo()
    if len(info.file_names) == 0:
        print("No files to remove.")
        return

    filtered_files = filter_filenames(info)
    files = (inquirer.prompt([inquirer.Checkbox('files', message="Select files to remove", choices=filtered_files)]) or {"files": "unknown"})

    for f in files['files']:
        info.file_names.remove(f)
        if os.path.exists(f):
            os.remove(f)

    info.save()

def filter_filenames(info: HugomanageInfo):
    filtered_files = []
    for f in info.file_names:
        if os.path.exists(f):
            filtered_files.append(f)
        else:
            info.file_names.remove(f)
    info.save()
    return filtered_files


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
