import os
import re

folder = '원본 해석/'
files = os.listdir(folder)

for f in sorted(files):
    filepath = os.path.join(folder, f)
    content = open(filepath, encoding='utf-8').read()
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.S)
    if match:
        yaml = match.group(1)
        cat_match = re.search(r'categories:\s*\[(.*?)\]', yaml)
        if cat_match:
            print(f"{f}: {cat_match.group(1)}")
