import os
import git
import json
import random,string

GIT_INFO_FILE = ".hugomanage"

class HugomanageInfo:
    def load_hugomanage_info(self):
        file = None
        if os.path.exists(GIT_INFO_FILE):
            file = open(GIT_INFO_FILE, 'r+')
        else:
            file = self.create_hugomanage_info()

        return json.loads(file.read())

    def create_hugomanage_info(self):
        file = open(GIT_INFO_FILE, 'w+')
        repo = git.Repo('./')

        default_info = {
            'is_branched': False,
            'original_branch': repo.active_branch.name,
            'branch_name': repo.active_branch.name,
            'file_names': []
        }

        json.dump(default_info, file)
        return file

    def set_info_key(self, key, val):
        info_file = open(GIT_INFO_FILE, "r+")
        info_dict = json.loads(info_file.read())
        info_dict[key] = val
        info_file.seek(0)
        info_file.truncate()
        json.dump(info_dict, info_file)


def create_branch():
    info = HugomanageInfo()
    repo = git.Repo('./')
    name = random_name
    new_branch = repo.create_head(random_name())
    new_branch.checkout
    info.set_info_key('branch_name', name)

def random_name():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(16))
   

