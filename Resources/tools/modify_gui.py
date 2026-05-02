import re
with open('c:/Users/osw/Desktop/Workspace/Projects/StepCode/Resources/tools/crawler_doingcoding_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Title change
content = content.replace('StepCode Reference 수집기 (GUI) - 접두어 패치판', 'DoingCoding 전용 수집기')

# 2. Domain var default to doingcoding
content = content.replace('self.domain_var = tk.StringVar(value=\"baekjoon\")', 'self.domain_var = tk.StringVar(value=\"doingcoding\")')

# 3. Modify _build_shared_settings
# Remove radio buttons
content = re.sub(r'tk\.Label\(\s*self\.shared_settings_frame,\s*text=\"\[ 타겟 도메인 \]\".*?self\.domain_var\.trace\(\"w\", self\.update_url_template\)', 'self.domain_var.trace(\"w\", self.update_url_template)', content, flags=re.DOTALL)

# Default URL template
content = content.replace('self.url_template.insert(0, \"https://www.acmicpc.net/problem/{id}\")', 'self.url_template.insert(0, \"http://edu.doingcoding.com/problem/{id}\")')

# 4. Modify update_url_template to only do doingcoding
new_update_url = '''    def update_url_template(self, *args):
        self.url_template.delete(0, tk.END)
        self.url_template.insert(0, \"http://edu.doingcoding.com/problem/{id}\")
        self._set_doingcoding_option_visibility()'''
content = re.sub(r'    def update_url_template\(self, \*args\):.*?def _set_doingcoding_option_visibility', new_update_url + '\n\n    def _set_doingcoding_option_visibility', content, flags=re.DOTALL)

# 5. Modify _set_doingcoding_option_visibility
new_visibility = '''    def _set_doingcoding_option_visibility(self):
        self.doingcoding_options_frame.pack(fill=\"x\", pady=(12, 0))
        self.check_light_mode.pack_forget()
        self.light_mode_var.set(False)'''
content = re.sub(r'    def _set_doingcoding_option_visibility\(self\):.*?def select_dir', new_visibility + '\n\n    def select_dir', content, flags=re.DOTALL)

# Default Prefix in _build_crawl_tab
content = content.replace('self.prefix_id.insert(0, \"\")', 'self.prefix_id.insert(0, \"ALLv\")')

# Remove scrape_baekjoon, scrape_baekjoon_light imports if present
content = re.sub(r'scrape_baekjoon,[\s\n]*scrape_baekjoon_light,[\s\n]*patch_file_badges,[\s\n]*analyze_badge_status,[\s\n]*has_special_badge,', '', content)

with open('c:/Users/osw/Desktop/Workspace/Projects/StepCode/Resources/tools/crawler_doingcoding_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
