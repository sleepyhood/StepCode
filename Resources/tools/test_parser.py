import sys
import os
import pprint
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from uploader_engine import parse_markdown

md_path = r"C:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\content\programming\doingcoding\LV26_재귀\02_workspace\ALLv05010_2111.md"
data = parse_markdown(md_path)

print("ID:", data['id'])
print("Title:", data['title'])
print("Tags:", data['tags'])
print("Desc Len:", len(data['description']))
print("InDesc Len:", len(data['input_desc']))
print("OutDesc Len:", len(data['output_desc']))
print("Hint Len:", len(data['hint']))
print(f"Samples count: {len(data['samples'])}")
for idx, s in enumerate(data['samples']):
    print(f" Sample {idx+1} IN len: {len(s[0])}, OUT len: {len(s[1])}")
