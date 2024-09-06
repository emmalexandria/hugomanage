import os
import git
import json
import random,string


class HugomanageInfo:
    FILENAME = ".hugomanage"

    repo: git.Repo
    is_branched: bool
    original_branch: str
    branch_name: str
    file_names: list 

    def __init__(self):
        self.load_or_create()

    def load_or_create(self):
        file = None
        if os.path.exists(self.FILENAME):
            file = open(self.FILENAME, 'r+')
        else:
            file = self._create_hugomanage_info()

        info = json.loads(file.read())

        self.repo = git.Repo('./')
        self.is_branched = info['is_branched']
        self.original_branch = info['original_branch']
        self.branch_name = info['branch_name']
        self.file_names = info['file_names']


    def _create_hugomanage_info(self):
        file = open(self.FILENAME, 'w+')
        repo = git.Repo('./')

        default_info = {
            'is_branched': False,
            'original_branch': repo.active_branch.name,
            'branch_name': repo.active_branch.name,
            'file_names': []
        }

        json.dump(default_info, file)
        return file

    def save(self):
        info = {
            'is_branched': self.is_branched,
            'original_branch': self.original_branch,
            'branch_name': self.branch_name,
            'file_names': self.file_names,
        }

        file = open(self.FILENAME, 'w+')
        file.seek(0)
        file.truncate()
        json.dump(info, file)
        file.close()


def create_branch(info: HugomanageInfo):
    repo = git.Repo('./')
    name = random_name()
    new_branch = repo.create_head(random_name())
    new_branch.checkout
    info.branch_name = name
    info.save()

def random_name():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(16))
   

