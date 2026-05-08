import os
import shutil
import re

base_dir = r"C:\Users\osw\Desktop\Workspace\Projects\StepCode\practice\data\content\programming\doingcoding\LV26_재귀"
dirs = {
    "ws": os.path.join(base_dir, "02_workspace"),
    "sol": os.path.join(base_dir, "03_solutions"),
    "tc": os.path.join(base_dir, "04_testcases")
}

target_map = {
    "519": "ALLv05001_519", "520": "SALLv05001_520",
    "521": "ALLv05002_521", "721": "SALLv05002_721",
    "522": "ALLv05003_522", "523": "SALLv05003_523",
    "526": "ALLv05004_526", "527": "SALLv05004_527",
    "N진수": "ALLv05005_LOCAL", "525": "SALLv05005_525",
    "문자열 거꾸로": "ALLv05006_LOCAL", "문자열 포장": "SALLv05006_LOCAL",
    "재귀 챗봇": "ALLv10001_LOCAL", "마트료시카": "SALLv10001_LOCAL",
    "524": "ALLv10002_524", "트리보나치": "SALLv10002_LOCAL",
    "1499": "ALLv10003_1499", "가중치 피보나치": "SALLv10003_LOCAL",
    "N자리 수 만들기": "ALLv10004_LOCAL", "1501": "SALLv10004_1501",
    "재귀의 귀재": "ALLv10005_LOCAL", "재귀의 함정": "SALLv10005_LOCAL",
}

def clean_title(title):
    return re.sub(r'^\d+\.\s*\[.*?\]\s*', '', title).strip().strip('"').strip("'")

# Find all MD files
all_mds = []
for root, _, files in os.walk(dirs['ws']):
    for f in files:
        if f.endswith('.md'):
            all_mds.append(os.path.join(root, f))

migration_plan = {}
for md_path in all_mds:
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    m_db = re.search(r'db_id:\s*(.*)', content)
    m_title = re.search(r'title:\s*(.*)', content)
    if not m_db or not m_title: continue
    
    db_id = m_db.group(1).strip()
    title = clean_title(m_title.group(1))
    
    target_base = None
    for k, v in target_map.items():
        if db_id == k: target_base = v; break
        if db_id == 'LOCAL' and k in title: target_base = v; break
    
    if target_base:
        # Prefer non-excluded (current) over excluded
        if target_base not in migration_plan or '99_excluded' in migration_plan[target_base]['md_src']:
            orig_base = os.path.basename(md_path).replace('.md', '')
            migration_plan[target_base] = {
                'md_src': md_path,
                'orig_base': orig_base,
                'title': title
            }

# Backup and clear main dirs
for name, p in dirs.items():
    bkp = p + "_bkp"
    if os.path.exists(bkp): shutil.rmtree(bkp)
    shutil.copytree(p, bkp)
    for item in os.listdir(p):
        if item not in ['99_excluded', 'images']:
            item_path = os.path.join(p, item)
            shutil.move(item_path, os.path.join(p, '99_excluded', item))

# Execute Migration
success_count = 0
for tgt, data in migration_plan.items():
    orig_base = data['orig_base']
    
    md_src = data['md_src'].replace('02_workspace', '02_workspace_bkp')
    with open(md_src, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'id:\s*.*', f"id: {tgt.split('_')[0]}", content)
    content = re.sub(r'title:\s*.*', f"title: \"{data['title']}\"", content)
    
    with open(os.path.join(dirs['ws'], tgt + '.md'), 'w', encoding='utf-8') as f:
        f.write(content)
        
    # 2. CPP & ZIP
    for ext, dname in [('.cpp', 'sol'), ('.zip', 'tc')]:
        src1 = os.path.join(dirs[dname], '99_excluded', orig_base + ext)
        src2 = os.path.join(dirs[dname], '_bkp', '99_excluded', orig_base + ext)
        tgt_path = os.path.join(dirs[dname], tgt + ext)
        if os.path.exists(src1):
            shutil.copy2(src1, tgt_path)
        elif os.path.exists(src2):
            shutil.copy2(src2, tgt_path)

    # Verification
    v1 = os.path.exists(os.path.join(dirs['ws'], tgt + '.md'))
    v2 = os.path.exists(os.path.join(dirs['sol'], tgt + '.cpp'))
    v3 = os.path.exists(os.path.join(dirs['tc'], tgt + '.zip'))
    if v1 and v2 and v3: success_count += 1

print(f"OK:{success_count}/{len(target_map)}")
