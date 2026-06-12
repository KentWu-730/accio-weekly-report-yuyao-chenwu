这是 Windows 侧的最小交付包。

zip 内保留 8 个文件：
1. windows_single_entry.txt
2. windows_master_handoff_short.txt
3. windows_master_handoff.txt
4. windows_codex_handoff_prompt_short.txt
5. windows_shop_context_template.json
6. windows_bundle_readme.txt
7. windows_evidence_commands.txt
8. windows_result_template.txt

直接给 Windows 侧 Codex 的唯一入口文件是 `windows_single_entry.txt`，把整段复制给它即可。
其他文件保留为拆分版和模板备份。

不要修改 Mac 侧的任何文件，也不要把 Mac 路径写进 Windows。
