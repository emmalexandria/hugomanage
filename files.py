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
        if os.path.exists(self.FILENAME) != True:
            self._create_hugomanage_info()

        file = open(self.FILENAME, "r+")
        
        info = json.loads(file.read())

        self.repo = git.Repo('./')
        self.is_branched = info['is_branched']
        self.original_branch = info['original_branch']
        self.branch_name = info['branch_name']
        self.file_names = info['file_names']

        file.close()


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
        file.close()

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


def create_branch(info: HugomanageInfo, repo: git.Repo, name: str):
    new_branch = repo.create_head(random_name())
    info.branch_name = name
    info.save()
    return new_branch

def checkout_active_branch(info: HugomanageInfo, repo: git.Repo):
    branch_name = info.branch_name
    branch = get_branch_by_name(info, repo, branch_name)   
    branch.checkout()

def merge_changes(info: HugomanageInfo, repo: git.Repo):
    repo.git.add('*')
    repo.git.commit("-m Add content")
    current_branch = repo.active_branch
    main_branch = get_branch_by_name(info, repo, info.original_branch)
    main_branch.checkout()
    o = repo.remotes.origin
    o.pull()

    repo.git.merge(current_branch)

def get_branch_by_name(info: HugomanageInfo, repo: git.Repo, name: str):
    branch = [b for b in repo.branches if b.name == name]
    if len(branch) == 0:
        branch = create_branch(info, repo, random_name())
    else:
        branch = branch[0]

    return branch

def random_name():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(16))
   

