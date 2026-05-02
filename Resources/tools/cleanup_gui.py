import re

file_path = 'c:/Users/osw/Desktop/Workspace/Projects/StepCode/Resources/tools/crawler_doingcoding_gui.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove light/dynamic mode variables
content = re.sub(r'        self.light_mode_var = tk.BooleanVar\(value=False\).*?\n', '', content)
content = re.sub(r'        self.dynamic_mode_var = tk.BooleanVar\(value=False\).*?\n', '', content)

# Remove _on_light_mode_toggle and _on_dynamic_mode_toggle
content = re.sub(r'    def _on_light_mode_toggle\(self\):.*?(?=    def _worker_loop)', '', content, flags=re.DOTALL)

# Add command to check_testcases and initialize state for admin entries
content = content.replace(
    'variable=self.get_testcases_var,\n        )',
    'variable=self.get_testcases_var,\n            command=self._on_testcases_toggle\n        )'
)

admin_init = """        self.admin_password.pack(side=tk.LEFT, padx=(5, 0))
        
        self.admin_username.config(state=tk.DISABLED)
        self.admin_password.config(state=tk.DISABLED)"""
content = content.replace('        self.admin_password.pack(side=tk.LEFT, padx=(5, 0))', admin_init)

# Remove light_mode/dynamic_mode checkbuttons
content = re.sub(r'        # 🚨 \[신규\] 배지 전용 라이트 모드 체크박스.*?command=self\._on_dynamic_mode_toggle,\n        \)\n        self\.check_dynamic_mode\.pack\(pady=4\)\n', '', content, flags=re.DOTALL)

# Remove visibility toggling for light mode
content = re.sub(r'        self\.check_light_mode\.pack_forget\(\)\n        self\.light_mode_var\.set\(False\)\n', '', content)

# Add _on_testcases_toggle method
toggle_method = """
    def _on_testcases_toggle(self):
        if self.get_testcases_var.get():
            self.admin_username.config(state=tk.NORMAL)
            self.admin_password.config(state=tk.NORMAL)
        else:
            self.admin_username.config(state=tk.DISABLED)
            self.admin_password.config(state=tk.DISABLED)

    def _build_crawl_tab(self):"""
content = content.replace('    def _build_crawl_tab(self):', toggle_method)

# Remove dynamic_mode and light_mode from _worker_loop definition
content = content.replace(
    'force_show_browser=False, skip_existing=True, light_mode=False, dynamic_mode=False):',
    'force_show_browser=False, skip_existing=True):'
)

# Replace the giant if dynamic_mode / elif light_mode / else block in _worker_loop with just the doingcoding engine call.
# Actually, since we only want doingcoding logic, we can just remove everything and only keep the doingcoding logic.
# Wait, it's easier to use python AST or regex to strip it.
# Let's write the whole _worker_loop replacement using a safer replace
loop_code_to_replace = re.search(r'(                    # 🚨 \[신규\] 라이트 모드 분기.*?                    else:\n)(                        # 도메인별 전용 엔진 호출)', content, flags=re.DOTALL)

if loop_code_to_replace:
    content = content.replace(loop_code_to_replace.group(1), '')

# Remove `if domain == "baekjoon":` branch
content = re.sub(r'                            if domain == "baekjoon":\n                                result = scrape_baekjoon\(target_url, save_dir=save_path, context=context\)\n                            else:\n                                # 학원 사이트 전용 엔진 호출 \(context를 browser 인자로 전달\)\n', '                            if True:\n', content)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

