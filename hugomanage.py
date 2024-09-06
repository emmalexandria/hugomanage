import frontmatter
import os
import sys
import inquirer
import argparse

from files import HugomanageInfo, create_branch

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

    print("Please fill out the following frontmatter fields:")
    new_frontmatter = (get_frontmatter_fields(example_post.metadata) or {})

    for key in new_frontmatter:
        if type(example_post.metadata[key]) == list:
            new_list = new_frontmatter[key].split(',')
            stripped_list = [j.strip() for j in new_list]
            example_post.metadata[key] = stripped_list 
        else:
            example_post.metadata[key] = new_frontmatter[key]

    example_post.content = ""

    output_text = frontmatter.dumps(example_post)

    filename = get_filename()
    path = content_type + "/" + filename

    while os.path.exists(path) and os.path.isdir(path) != True:
        print("File already exists, please enter another name")
        filename = get_filename()
        path = content_type + "/" + filename



def sync_changes():
    return

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
    subdirs.append('content')

    return subdirs

def get_frontmatter_fields(metadata):
    fields = []
    for key in metadata: 
        if type(metadata[key]) == dict:
            for key2 in metadata[key]:
                fields = gen_field_question(metadata[key], key2, fields, prefix=key)        

        fields = gen_field_question(metadata, key, fields)        

    return inquirer.prompt(fields)

def gen_field_question(metadata, key, fields, **kwargs):
    prefix = kwargs.get('prefix', "") 
    if prefix != "":
        prefix += "/"
    if type(metadata[key]) == list:
        default = (item[1: -1] for item in str(metadata[key])[1: -1].split(','))
        fields.append(
            inquirer.Text(key, message="Enter comma seperated list for " + prefix + key, default=default)
        )
    else:
        fields.append(
            inquirer.Text(key, message="Enter value for " + prefix  + key, default=metadata[key])
        )

    return fields



if __name__ == "__main__":
    main()
