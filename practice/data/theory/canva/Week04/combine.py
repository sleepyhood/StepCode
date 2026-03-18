import json

with open(r'C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week04\final_match.json', 'r', encoding='utf-8') as f:
    part1 = json.load(f)

# Using final_match4.json which has proper UTF-8 format
with open(r'C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week04\final_match4.json', 'r', encoding='utf-8') as f:
    part2 = json.load(f)

combined = {}
combined.update(part1)
combined.update(part2)

with open(r'C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory\canva\Week04\final_match_complete.json', 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print("Done")
