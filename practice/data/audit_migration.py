import os

BASE_DIR = r"C:\Users\osw\Desktop\Workspace\#Projects\StepCode\practice\data"
THEORY_DIR = os.path.join(BASE_DIR, "theory", "language")
SETS_DIR = os.path.join(BASE_DIR, "sets", "language")
V2_DIR = os.path.join(BASE_DIR, "language_v2")

def audit():
    print("=== MIGRATION AUDIT REPORT ===")
    
    # Check Theory files
    theory_files = [f for f in os.listdir(THEORY_DIR) if f.endswith('.md')]
    print(f"1. Original Theory/Guide Files: {len(theory_files)}")
    
    # Check Set files
    set_files = [f for f in os.listdir(SETS_DIR) if f.endswith('.json')]
    print(f"2. Original JSON Problem Sets: {len(set_files)}")
    
    # Check v2 Docs
    v2_docs = []
    v2_sets = []
    
    for root, dirs, files in os.walk(V2_DIR):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, V2_DIR)
                if "_docs" in rel_path:
                    v2_docs.append(rel_path)
                else:
                    v2_sets.append(rel_path)
                    
    print(f"\n3. Migrated Theory/Guide (in _docs): {len(v2_docs)}")
    print(f"4. Migrated Problem Sets (.md): {len(v2_sets)}")
    
    # Check for missing docs
    if len(theory_files) != len(v2_docs):
        print(f"WARNING: Theory files count mismatch! Expected {len(theory_files)}, found {len(v2_docs)}")
        print(f"[Details] Found docs: {v2_docs}")
        
    # Check for missing sets
    if len(set_files) != len(v2_sets):
        print(f"WARNING: Problem sets count mismatch! Expected {len(set_files)}, found {len(v2_sets)}")
        
    print("\n[Sanity Check Details]")
    # Spot-check some known edge cases
    expected_java = "lv06_if\\java\\b01.md"
    if expected_java in v2_sets or expected_java.replace('\\', '/') in [s.replace('\\', '/') for s in v2_sets]:
        print("PASS: java_if_b1 correctly mapped to lv06_if/java/b01.md")
    else:
        print("FAIL: java_if_b1 mapping failed.")
        
    # Check array2d docs merge
    expected_array2d_docs = [s for s in v2_docs if "lv15_array2d" in s and "_docs" in s]
    if len(expected_array2d_docs) >= 2:
        print("PASS: array2d theory & guide correctly merged into lv15_array2d/_docs")
    else:
        print(f"FAIL: array2d _docs mapping issue. Found: {expected_array2d_docs}")

    # Identify any orphan or misnamed topics
    topics = os.listdir(V2_DIR)
    print(f"\nDiscovered Topics in V2: {topics}")
    for t in topics:
        if "array" in t and "lv" not in t:
             print(f"WARNING: Possible unmerged topic found: {t}")

if __name__ == '__main__':
    audit()
