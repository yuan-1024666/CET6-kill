#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analyze what derivative/phrase translations are missing in word_meanings.json"""
import os, json, re, sys
sys.path.insert(0, r'f:\66666\docs')

# Load gen.py's DERIVATIVES and REAL_PHRASES
gen_text = open(r'f:\66666\docs\gen.py', 'r', encoding='utf-8').read()

# Extract DERIVATIVES dict
start = gen_text.find('# ===== 同根词映射表 =====')
end = gen_text.find('# ===== 短语映射表 =====')
deriv_section = gen_text[start:end]
# Extract the dict between the marker and REAL_PHRASES marker
dict_start = deriv_section.index('DERIVATIVES = {')
dict_end = deriv_section.rindex('}')
deriv_code = deriv_section[dict_start:dict_end+1]
DERIVATIVES = {}
exec(deriv_code, {}, {'DERIVATIVES': DERIVATIVES})
DERIVATIVES = DERIVATIVES.get('DERIVATIVES', DERIVATIVES)
# Fix: exec assigns to global, reassign
# It didn't work cleanly. Let me parse manually
pass

# Actually, let me just count by reading the text directly
# Count derivative entries (base word keys)
deriv_bases = set()
deriv_words = set()
for line in deriv_section.split('\n'):
    match = re.match(r"\s+'(\w+)':\s*\{", line)
    if match:
        deriv_bases.add(match.group(1))

# Count phrase entries
phr_section = gen_text[gen_text.find('# ===== 短语映射表 ====='):gen_text.find('# ===== Build WORD_BANK JS')]
phr_bases = set()
phr_phrases = set()
for line in phr_section.split('\n'):
    # Match lines like: 'abandon': ['abandon ship', ...
    match = re.match(r"\s+'(\w+)':\s*\[", line)
    if match:
        phr_bases.add(match.group(1))
    # Also count individual phrases
    pmatches = re.findall(r"'([a-z][^']*)'", line)
    for pm in pmatches:
        if ' ' in pm and len(pm) > 3:  # looks like a phrase
            phr_phrases.add(pm)

print(f"Derivative bases in gen.py: {len(deriv_bases)}")
print(f"Phrase bases in gen.py: {len(phr_bases)}")
print(f"Total unique phrases: {len(phr_phrases)}")

# Load word_meanings.json
wm_path = r'f:\66666\docs\data\word_meanings.json'
raw = open(wm_path, 'rb').read()
wm = json.loads(raw.decode('gb18030'))
deriv_trans = wm.get('derivatives', {})
phr_trans = wm.get('phrases', {})

print(f"\nTranslations in word_meanings.json:")
print(f"  Derivative words with translations: {len(deriv_trans)}")
print(f"  Phrase bases with translations: {len(phr_trans)}")

# Count total phrase translations
total_phr_trans = sum(len(v) if isinstance(v, list) else sum(len(p) for p in v.values()) for v in phr_trans.values())
phrase_key_count = sum(len(v) if isinstance(v, dict) else 1 for v in phr_trans.values() if phr_trans.values())
# Actually, phr_trans is {word: {phrase: [meanings]}}
total_phrase_keys = sum(len(v) for v in phr_trans.values() if isinstance(v, dict))
print(f"  Total phrase keys translated: {total_phrase_keys}")

# What derivatives have translations?
deriv_with_trans = set(deriv_trans.keys())
print(f"\nDerivative words WITH translations: {len(deriv_with_trans)}")
print(f"Sample: {list(deriv_with_trans)[:20]}")

# What's missing?
all_deriv_words = set()
for base in deriv_bases:
    # Read actual derivative words from gen.py
    pass

print(f"\n=== Key insight ===")
print(f"gen.py defines ~{len(deriv_bases)} base words with derivatives")
print(f"word_meanings.json has translations for {len(deriv_trans)} derivative words")
print(f"gen.py defines ~{len(phr_bases)} words with phrases")
print(f"word_meanings.json has phrase translations for {len(phr_trans)} words")