import os, re

d = r'f:\66666\docs'
# find txt files
for f in os.listdir(d):
    if f.endswith('.txt') and '乱序' in f:
        src = os.path.join(d, f)
        break

raw = open(src, 'rb').read()
text = None
for enc in ['gb18030', 'gbk', 'utf-8']:
    try:
        text = raw.decode(enc)
        print(f"Decoded with {enc}")
        break
    except:
        continue

lines = text.split('\n')
words = set()
for line in lines:
    line = line.strip()
    if not line or len(line) < 5 or '\t' not in line:
        continue
    parts = line.split('\t')
    first = parts[0].strip()
    wm = re.match(r'^([a-z\-]+)', first, re.I)
    if not wm:
        continue
    word = wm.group(1).strip().lower()
    if len(word) >= 2 and re.search(r'[aeiou]', word):
        words.add(word)

print(f"Total unique words: {len(words)}")
print(f"Sample: {list(words)[:10]}")