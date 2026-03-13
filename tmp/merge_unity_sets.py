import os
import json

base_path = r'c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\sets\unity'
index_path = r'c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\sets.index.json'
theory_index_path = r'c:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data\theory.index.json'

def merge_sets():
    # 1. Group files by category
    files = os.listdir(base_path)
    groups = {}
    for f in files:
        if not f.endswith('.json'): continue
        if '_b01.json' not in f and '_c01.json' not in f: continue
        
        # Example: unity_u01_inspector_b01.json -> unity_u01_inspector
        cat_id = f.replace('_b01.json', '').replace('_c01.json', '')
            
        if cat_id not in groups: groups[cat_id] = []
        groups[cat_id].append(f)
    
    new_sets_info = {} # cat_id -> new_info

    # 2. Merge each group
    for cat_id, f_list in groups.items():
        # Sort to put basic first, then challenge
        f_list.sort()
        
        combined_problems = []
        seen_ids = set()
        
        main_title = ""
        
        for f in f_list:
            full_path = os.path.join(base_path, f)
            with open(full_path, 'r', encoding='utf-8-sig') as jf:
                data = json.load(jf)
                if not main_title:
                    main_title = data.get('title', '').replace(' 기초 1회차', '').replace(' Basic R1', '')
                
                for p in data.get('problems', []):
                    if p['id'] not in seen_ids:
                        combined_problems.append(p)
                        seen_ids.add(p['id'])
        
        # Sort problems by ID (p01, p02, x01, x02...)
        combined_problems.sort(key=lambda x: x['id'])
        
        new_id = cat_id
        new_filename = f"{cat_id}.json"
        
        new_data = {
            "id": new_id,
            "title": main_title,
            "categoryId": cat_id,
            "availableLanguages": ["csharp"],
            "problems": combined_problems
        }
        
        with open(os.path.join(base_path, new_filename), 'w', encoding='utf-8') as outf:
            json.dump(new_data, outf, ensure_ascii=False, indent=4)
            
        new_sets_info[cat_id] = {
            "id": new_id,
            "categoryId": cat_id,
            "title": main_title,
            "numProblems": len(combined_problems),
            "file": f"unity/{new_filename}"
        }
        print(f"Merged {cat_id} with {len(combined_problems)} problems.")

    # 3. Update sets.index.json
    with open(index_path, 'r', encoding='utf-8') as f:
        sets_index = json.load(f)
    
    new_index = []
    processed_cats = set()
    
    for entry in sets_index:
        cat_id = entry.get('categoryId')
        if cat_id in new_sets_info:
            if cat_id not in processed_cats:
                new_entry = {
                    "id": new_sets_info[cat_id]["id"],
                    "categoryId": cat_id,
                    "title": new_sets_info[cat_id]["title"],
                    "round": 1,
                    "difficulty": "combined",
                    "numProblems": new_sets_info[cat_id]["numProblems"],
                    "file": new_sets_info[cat_id]["file"]
                }
                new_index.append(new_entry)
                processed_cats.add(cat_id)
        else:
            new_index.append(entry)
            
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(new_index, f, ensure_ascii=False, indent=4)

    # 4. Update theory.index.json
    with open(theory_index_path, 'r', encoding='utf-8') as f:
        theory_index = json.load(f)
        
    for entry in theory_index:
        cat_id = entry.get('categoryId')
        if cat_id in new_sets_info:
            entry['recommendedSetId'] = new_sets_info[cat_id]["id"]
            entry['relatedSetIds'] = [new_sets_info[cat_id]["id"]]
            
    with open(theory_index_path, 'w', encoding='utf-8') as f:
        json.dump(theory_index, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    merge_sets()
