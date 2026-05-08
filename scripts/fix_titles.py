import os
import re

d = r'C:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\content\programming\doingcoding\LV26_재귀\02_workspace'

for f in os.listdir(d):
    if f.endswith('.md'):
        path = os.path.join(d, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Add newline back
        new_content = re.sub(r'title:\s*"(.*)"platform:', r'title: "\1"\nplatform:', content)
        
        if content != new_content:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)
        
        print(f"Fixed newline {f}")
