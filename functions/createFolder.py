import os

def createFolder(folder_structure):
    if not os.path.exists(folder_structure):
        os.makedirs(folder_structure)
        print(f'new folder created:  {folder_structure}')
