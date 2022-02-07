import os

OBSIDIAN_DIR = '/Users/newdev/Google Drive/Folders/obsidian-vaults/neel-nandas-blog'

markdown_files = [
    file for file in
    os.listdir('/Users/newdev/Google Drive/Folders/obsidian-vaults/neel-nandas-blog')
    if '.md' in file
]

for file in markdown_files:
    with open(f"{OBSIDIAN_DIR}/{file}", 'r') as f:
        file_str = f.read()

        if 'Content of Post' not in file_str:
            print(f"{file} has # Content of Post? {'Content of Post' in file_str}")
            print('\n')
        if 'External References' not in file_str:
            print(f"{file} has External References? {'External References' in file_str}")
            print('\n')



