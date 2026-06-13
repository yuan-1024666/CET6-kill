# -*- coding: utf-8 -*-
import re
import random

# 使用 latin1 编码读取（latin1 可以读取任何字节）
with open('f:/66666/66666/index.html', 'r', encoding='latin1', errors='ignore') as f:
    content = f.read()

# 提取所有单词数据
word_pattern = r'\{word:"([^"]+)",phonetic:"([^"]+)",pos:"([^"]+)",segments:\[([^\]]+(?:\[[^\]]*\])?[^}]*)\]\}'
words = re.findall(word_pattern, content)

print(f"总单词数: {len(words)}")
print("=" * 80)

# 检查各种情况
issues = {
    'no_derivative': [],      # 无同根词
    'no_phrase': [],          # 无短语
    'same_answer': [],        # 答案相同
    'correct': [],            # 正确
}

for word, phonetic, pos, segments_str in words:
    # 提取segments
    seg_pattern = r'\{"text": "([^"]+)", "label": "([^"]+)", "answer": (\[[^\]]+\])'
    segments = re.findall(seg_pattern, segments_str)

    if len(segments) >= 3:
        seg1_text, seg1_label, seg1_ans = segments[0]
        seg2_text, seg2_label, seg2_ans = segments[1]
        seg3_text, seg3_label, seg3_ans = segments[2]

        # 检查同根词和短语
        is_derivative = '同根词' in seg2_label
        is_phrase = '短语' in seg3_label

        if not is_derivative:
            issues['no_derivative'].append(word)
        if not is_phrase:
            issues['no_phrase'].append(word)

        # 检查答案是否相同
        if seg1_ans == seg2_ans == seg3_ans:
            issues['same_answer'].append(word)
        else:
            issues['correct'].append(word)

print(f"\n? 正确格式: {len(issues['correct'])} 个")
print(f"? 无同根词: {len(issues['no_derivative'])} 个")
print(f"? 无短语: {len(issues['no_phrase'])} 个")
print(f"? 答案全相同: {len(issues['same_answer'])} 个")

# 显示示例
print("\n" + "=" * 80)
print("? 随机抽查 10 个正确示例:")
print("=" * 80)

sample_correct = random.sample(issues['correct'], min(10, len(issues['correct'])))
for word in sample_correct:
    # 找到该单词的数据
    for w, phonetic, pos, segments_str in words:
        if w == word:
            segments = re.findall(seg_pattern, segments_str)
            print(f"\n【{word}】({pos})")
            for text, label, answer in segments:
                print(f"  {label}: {text} → {answer}")
            break

# 显示问题示例
if issues['no_derivative']:
    print("\n" + "=" * 80)
    print("?? 无同根词示例 (前5个):")
    print("=" * 80)
    for word in issues['no_derivative'][:5]:
        for w, phonetic, pos, segments_str in words:
            if w == word:
                segments = re.findall(seg_pattern, segments_str)
                print(f"\n【{word}】({pos})")
                for text, label, answer in segments:
                    print(f"  {label}: {text} → {answer}")
                break

if issues['same_answer']:
    print("\n" + "=" * 80)
    print("?? 答案全相同示例 (前5个):")
    print("=" * 80)
    for word in issues['same_answer'][:5]:
        for w, phonetic, pos, segments_str in words:
            if w == word:
                segments = re.findall(seg_pattern, segments_str)
                print(f"\n【{word}】({pos})")
                for text, label, answer in segments:
                    print(f"  {label}: {text} → {answer}")
                break
