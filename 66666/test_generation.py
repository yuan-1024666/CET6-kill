# -*- coding: utf-8 -*-
import re

with open('f:/66666/66666/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查几个例子
words_to_check = ['reliable', 'consistent', 'transform', 'demonstrate', 'eliminate', 'hush']

for word in words_to_check:
    pattern = r'\{word:\"' + word + r'\"[^\}]+\}'
    match = re.search(pattern, content)
    if match:
        print(f'=== {word} ===')
        # 查找所有segment
        seg_pattern = r'\{\"text\": \"([^\"]+)\", \"label\": \"([^\"]+)\", \"answer\": (\[[^\]]+\])'
        segments = re.findall(seg_pattern, match.group())
        for text, label, answer in segments:
            print(f'  {label}: {text} -> {answer}')
        print()
