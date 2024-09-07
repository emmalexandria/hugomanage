import os
import git
import json
import random,string


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


def merge_changes(info: HugomanageInfo, repo: git.Repo):
    branch_name = gen_branch_name(info)
    print(branch_name)
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()
    repo.git.add(info.file_names)
    repo.git.commit("-m Add content")
    o = repo.remotes.origin
    o.push()

    info.file_names = []
    info.save()

def gen_branch_name(info: HugomanageInfo):
    branch_name = ""
    first_loop = True
    for name in info.file_names:
        new_name = name
        new_name = new_name.lower()
        new_name = new_name.replace(' ', '_')
        if first_loop != True:
            branch_name += '+'
        branch_name += new_name
        first_loop = False

    return branch_name
