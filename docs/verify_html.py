# -*- coding: utf-8 -*-
import re

html = open(r'f:\66666\docs\index.html','r',encoding='utf-8').read()

print("=== Verifying accurate translations in index.html ===")
print()

# Check derivatives
checks = {
    'preservation': '保存',
    'achievement': '成就',
    'fascinating': '迷人',
    'convincing': '信服',
    'domination': '统治',
    'elimination': '消除',
    'hushed': '安静',
    'reliability': '可靠',
    'dedication': '奉献',  # from devote
    'concentration': '集中',
}
for word, ch in checks.items():
    idx = html.find('"' + word + '"')
    if idx >= 0:
        snippet = html[idx:idx+250]
        if ch in snippet:
            print(f"  [OK] {word}: contains '{ch}' -> PASS")
        else:
            cns = re.findall(r'"answer":\s*\[([^\]]*)\]', snippet)
            print(f"  [??] {word}: answer={cns[0][:80] if cns else 'N/A'}")
    else:
        print(f"  [--] {word}: not found")

print()
print("=== Phrase checks ===")
phr_checks = {
    'preserve food': '食物',
    'commit a crime': '犯罪',
    'abandon ship': '弃船',
    'take charge of': '负责',
    'concentrate on': '集中',
    'cope with': '应对',
}
for phrase, ch in phr_checks.items():
    idx = html.find(phrase)
    if idx >= 0:
        snippet = html[idx-20:idx+200]
        if ch in snippet:
            print(f"  [OK] '{phrase}': contains '{ch}' -> PASS")
        else:
            print(f"  [??] '{phrase}': found but NO '{ch}'")
    else:
        print(f"  [--] '{phrase}': NOT FOUND")

print()
print(f"HTML size: {len(html)//1024} KB")
print(f"WORD_BANK words: {html.count('word:\"')}")
print(f"衍生词 segments: {html.count('同根词')}")
print(f"短语 segments: {html.count('短语')}")
print()
print("Done!")