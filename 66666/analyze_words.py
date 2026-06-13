# -*- coding: utf-8 -*-
import re

# 读取词库数据
with open('f:/66666/66666/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 统计有多少单词使用了'用法'标签（表示没有同根词）
segments = re.findall(r'segments:\[([^\]]+)\]', content)

count_no_derivative = 0
count_no_phrase = 0
total_words = len(segments)

for seg in segments:
    if '"label": "用法"' in seg:
        count_no_derivative += 1
    if '"label": "词义3"' in seg:
        count_no_phrase += 1

print(f'总单词数: {total_words}')
print(f'无同根词（使用"用法"标签）: {count_no_derivative}')
print(f'无真实短语（使用"词义3"）: {count_no_phrase}')
