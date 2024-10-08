import os
import git
import json
import random,string
import platform, subprocess


class HugomanageInfo:
    FILENAME = ".hugomanage"

    repo: git.Repo
    file_names: list 

    def __init__(self):
        self.load_or_create()

    def load_or_create(self):
        if os.path.exists(self.FILENAME) != True:
            self._create_hugomanage_info()

        file = open(self.FILENAME, "r+")
        
        info = json.loads(file.read())

        self.repo = git.Repo('./')
        self.file_names = info['file_names']

        file.close()


    def _create_hugomanage_info(self):
        file = open(self.FILENAME, 'w+')
        repo = git.Repo('./')

        default_info = {
            'file_names': []
        }

        json.dump(default_info, file)
        file.close()

    def save(self):
        info = {
            'file_names': self.file_names,
        }

        file = open(self.FILENAME, 'w+')
        file.seek(0)
        file.truncate()
        json.dump(info, file)
        file.close()

    def remove_missing_files(self):
        for file in self.file_names:
            if os.path.exists(file) != True:
                self.file_names.remove(file)
        
        self.save()

def merge_changes(info: HugomanageInfo, repo: git.Repo):
    info.remove_missing_files()

    branch_name = gen_branch_name(info)
    print(branch_name)
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()
    for file in info.file_names:
        repo.git.add(file)
    repo.git.commit("-m Add content")
    repo.git.push('--set-upstream', 'origin', new_branch)

    info.file_names = []
    info.save()

def open_file_in_editor(filepath: str):
    system_platform = platform.system()

    try:
        if system_platform == 'Windows':  # For Windows
            os.startfile(filepath)
        elif system_platform == 'Darwin':  # For macOS
            subprocess.run(['open', filepath])
        else:  # For Linux and other Unix-based systems
            subprocess.run(['xdg-open', filepath])
        print(f"Opened {filepath} successfully.")
    except Exception as e:
        print(f"Failed to open {filepath}: {e}")

def gen_branch_name(info: HugomanageInfo):
    branch_name = ""
    first_loop = True
    for name in info.file_names:
        new_name = os.path.basename(name)
        new_name = new_name.lower()
        new_name = new_name.replace(' ', '_')
        if first_loop != True:
            branch_name += '+'
        branch_name += new_name
        first_loop = False

    return branch_name
