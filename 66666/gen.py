# Generator v11: 真同根词only | 每段答案独立分配 | 无假词
import os, json, re

d = r'f:\66666\66666'
txt_files = [f for f in os.listdir(d) if f.endswith('.txt') and 'parsed' not in f.lower() and 'json' not in f.lower()]
src = os.path.join(d, txt_files[0])
raw = open(src, 'rb').read()

text = None
for enc in ['gb18030', 'gbk', 'utf-8']:
    try:
        text = raw.decode(enc)
        if '\u7684' in text: print(f"Decoded with {enc}"); break
    except: continue
if text is None: text = raw.decode('gb18030', errors='replace')

lines = text.split('\n')
parsed = {}
for line in lines:
    line = line.strip()
    if not line or len(line) < 5 or '\t' not in line: continue
    parts = line.split('\t')
    if len(parts) < 2: continue
    first = parts[0].strip()
    wm = re.match(r'^([a-z\-]+)', first, re.I)
    if not wm: continue
    word = wm.group(1).strip().lower()
    if len(word) < 2 or not re.search(r'[aeiou]', word): continue
    rest = ' '.join(parts[1:]).strip()
    pos = ''
    mp = re.match(r'^((?:[nvadj]+\.\s*)+)\s*', rest, re.I)
    if mp: pos = mp.group(1).strip(); rest = rest[mp.end():].strip()
    else:
        p = re.match(r'^(n\.|v\.|adj\.|adv\.|prep\.|pron\.|conj\.|int\.|abbr\.|num\.|art\.|vi\.|vt\.)\s*', rest, re.I)
        if p: pos = p.group(1).strip(); rest = rest[p.end():].strip()
    rest = re.sub(r'\[.*?\]', '', rest).strip()
    if len(rest) < 2 or not re.search(r'[\u4e00-\u9fff]', rest): continue
    meanings = re.split(r'[；;,，、]', rest)
    meanings = [m.strip() for m in meanings if m.strip() and re.search(r'[\u4e00-\u9fff]', m)]
    if not meanings: continue
    if word in parsed:
        if pos and not parsed[word]['pos']: parsed[word]['pos'] = pos
        for m in meanings:
            if m not in parsed[word]['meanings']: parsed[word]['meanings'].append(m)
    else:
        parsed[word] = {'word': word, 'pos': pos, 'meanings': meanings}

words_list = list(parsed.values())
print(f"Parsed {len(words_list)} unique words")

# ===== 同根词映射表 =====
DERIVATIVES = {
    'abandon': {'abandonment': 'n.', 'abandoned': 'adj.'},
    'absorb': {'absorption': 'n.', 'absorbed': 'adj.'},
    'abstract': {'abstraction': 'n.', 'abstractly': 'adv.'},
    'abundant': {'abundance': 'n.', 'abundantly': 'adv.'},
    'accelerate': {'acceleration': 'n.', 'accelerating': 'adj.'},
    'accurate': {'accuracy': 'n.', 'accurately': 'adv.'},
    'achieve': {'achievement': 'n.', 'achievable': 'adj.'},
    'acknowledge': {'acknowledgement': 'n.'},
    'acquire': {'acquisition': 'n.', 'acquired': 'adj.'},
    'adapt': {'adaptation': 'n.', 'adaptable': 'adj.'},
    'addict': {'addiction': 'n.', 'addictive': 'adj.'},
    'adjust': {'adjustment': 'n.', 'adjustable': 'adj.'},
    'admire': {'admiration': 'n.', 'admirable': 'adj.'},
    'adopt': {'adoption': 'n.', 'adoptive': 'adj.'},
    'affect': {'affection': 'n.', 'affected': 'adj.'},
    'allocate': {'allocation': 'n.'},
    'alter': {'alteration': 'n.', 'alternative': 'adj.'},
    'amaze': {'amazement': 'n.', 'amazing': 'adj.'},
    'anticipate': {'anticipation': 'n.'},
    'anxious': {'anxiety': 'n.', 'anxiously': 'adv.'},
    'apply': {'application': 'n.', 'applicable': 'adj.'},
    'appreciate': {'appreciation': 'n.', 'appreciative': 'adj.'},
    'approach': {'approachable': 'adj.'},
    'approve': {'approval': 'n.', 'approved': 'adj.'},
    'argue': {'argument': 'n.', 'argumentative': 'adj.'},
    'arrange': {'arrangement': 'n.'},
    'assess': {'assessment': 'n.'},
    'assign': {'assignment': 'n.', 'assigned': 'adj.'},
    'assist': {'assistance': 'n.', 'assistant': 'n.'},
    'assume': {'assumption': 'n.'},
    'attach': {'attachment': 'n.', 'attached': 'adj.'},
    'attend': {'attendance': 'n.', 'attendant': 'n.'},
    'attract': {'attraction': 'n.', 'attractive': 'adj.'},
    'aware': {'awareness': 'n.'},
    'balance': {'balanced': 'adj.'},
    'bear': {'bearable': 'adj.', 'unbearable': 'adj.'},
    'benefit': {'beneficial': 'adj.', 'beneficiary': 'n.'},
    'bore': {'boredom': 'n.', 'boring': 'adj.'},
    'bound': {'boundary': 'n.', 'unbound': 'adj.'},
    'brief': {'briefly': 'adv.', 'brevity': 'n.'},
    'capable': {'capability': 'n.', 'incapable': 'adj.'},
    'capture': {'captive': 'n.', 'captivity': 'n.'},
    'caution': {'cautious': 'adj.', 'cautiously': 'adv.'},
    'celebrate': {'celebration': 'n.', 'celebrated': 'adj.'},
    'challenge': {'challenging': 'adj.'},
    'classify': {'classification': 'n.', 'classified': 'adj.'},
    'collapse': {'collapsed': 'adj.', 'collapsible': 'adj.'},
    'combine': {'combination': 'n.', 'combined': 'adj.'},
    'commit': {'commitment': 'n.', 'committed': 'adj.'},
    'communicate': {'communication': 'n.'},
    'compare': {'comparison': 'n.', 'comparable': 'adj.'},
    'compensate': {'compensation': 'n.'},
    'compete': {'competition': 'n.', 'competitive': 'adj.'},
    'complain': {'complaint': 'n.'},
    'complete': {'completion': 'n.', 'completely': 'adv.'},
    'complex': {'complexity': 'n.'},
    'compose': {'composition': 'n.', 'composer': 'n.'},
    'concentrate': {'concentration': 'n.', 'concentrated': 'adj.'},
    'concern': {'concerning': 'prep.', 'concerned': 'adj.'},
    'conclude': {'conclusion': 'n.', 'conclusive': 'adj.'},
    'conduct': {'conductor': 'n.', 'conductive': 'adj.'},
    'confirm': {'confirmation': 'n.', 'confirmed': 'adj.'},
    'confuse': {'confusion': 'n.', 'confused': 'adj.'},
    'connect': {'connection': 'n.', 'connected': 'adj.'},
    'conscious': {'consciousness': 'n.', 'unconscious': 'adj.'},
    'conserve': {'conservation': 'n.', 'conservative': 'adj.'},
    'consider': {'consideration': 'n.', 'considerable': 'adj.'},
    'consist': {'consistent': 'adj.', 'consistency': 'n.'},
    'construct': {'construction': 'n.', 'constructive': 'adj.'},
    'consume': {'consumption': 'n.', 'consumer': 'n.'},
    'contain': {'container': 'n.'},
    'contribute': {'contribution': 'n.', 'contributor': 'n.'},
    'convenient': {'convenience': 'n.'},
    'convince': {'convincing': 'adj.', 'convinced': 'adj.'},
    'cooperate': {'cooperation': 'n.', 'cooperative': 'adj.'},
    'correspond': {'correspondence': 'n.', 'corresponding': 'adj.'},
    'create': {'creation': 'n.', 'creative': 'adj.'},
    'criticize': {'criticism': 'n.', 'critical': 'adj.'},
    'curious': {'curiosity': 'n.', 'curiously': 'adv.'},
    'damage': {'damaging': 'adj.', 'damaged': 'adj.'},
    'debate': {'debatable': 'adj.'},
    'decide': {'decision': 'n.', 'decisive': 'adj.'},
    'declare': {'declaration': 'n.'},
    'decline': {'declining': 'adj.'},
    'decorate': {'decoration': 'n.', 'decorative': 'adj.'},
    'defend': {'defense': 'n.', 'defensive': 'adj.'},
    'define': {'definition': 'n.', 'definitive': 'adj.'},
    'deliver': {'delivery': 'n.', 'delivered': 'adj.'},
    'demand': {'demanding': 'adj.'},
    'demonstrate': {'demonstration': 'n.'},
    'depend': {'dependence': 'n.', 'dependent': 'adj.'},
    'depress': {'depression': 'n.', 'depressed': 'adj.'},
    'describe': {'description': 'n.', 'descriptive': 'adj.'},
    'deserve': {'deserving': 'adj.'},
    'design': {'designer': 'n.', 'designed': 'adj.'},
    'destroy': {'destruction': 'n.', 'destructive': 'adj.'},
    'determine': {'determination': 'n.', 'determined': 'adj.'},
    'develop': {'development': 'n.', 'developing': 'adj.'},
    'devote': {'devotion': 'n.', 'devoted': 'adj.'},
    'differ': {'difference': 'n.', 'different': 'adj.'},
    'direct': {'direction': 'n.', 'directly': 'adv.'},
    'discover': {'discovery': 'n.'},
    'discuss': {'discussion': 'n.'},
    'distinct': {'distinction': 'n.', 'distinctive': 'adj.'},
    'distinguish': {'distinguished': 'adj.'},
    'distribute': {'distribution': 'n.'},
    'divide': {'division': 'n.', 'divided': 'adj.'},
    'dominate': {'domination': 'n.', 'dominant': 'adj.'},
    'doubt': {'doubtful': 'adj.', 'undoubtedly': 'adv.'},
    'economy': {'economic': 'adj.', 'economical': 'adj.'},
    'educate': {'education': 'n.', 'educational': 'adj.'},
    'effective': {'effectively': 'adv.', 'effectiveness': 'n.'},
    'efficient': {'efficiency': 'n.', 'efficiently': 'adv.'},
    'eliminate': {'elimination': 'n.'},
    'emerge': {'emergence': 'n.', 'emerging': 'adj.'},
    'emotion': {'emotional': 'adj.', 'emotionally': 'adv.'},
    'emphasize': {'emphasis': 'n.', 'emphatic': 'adj.'},
    'employ': {'employment': 'n.', 'employer': 'n.', 'employee': 'n.'},
    'encourage': {'encouragement': 'n.', 'encouraging': 'adj.'},
    'engage': {'engagement': 'n.', 'engaged': 'adj.'},
    'enhance': {'enhancement': 'n.', 'enhanced': 'adj.'},
    'enjoy': {'enjoyment': 'n.', 'enjoyable': 'adj.'},
    'entertain': {'entertainment': 'n.', 'entertaining': 'adj.'},
    'enthusiasm': {'enthusiastic': 'adj.'},
    'environment': {'environmental': 'adj.'},
    'establish': {'establishment': 'n.', 'established': 'adj.'},
    'evaluate': {'evaluation': 'n.'},
    'evidence': {'evident': 'adj.', 'evidently': 'adv.'},
    'evolve': {'evolution': 'n.', 'evolving': 'adj.'},
    'examine': {'examination': 'n.'},
    'except': {'exception': 'n.', 'exceptional': 'adj.'},
    'excite': {'excitement': 'n.', 'exciting': 'adj.'},
    'exclude': {'exclusion': 'n.', 'exclusive': 'adj.'},
    'execute': {'execution': 'n.', 'executive': 'n.'},
    'exhibit': {'exhibition': 'n.'},
    'exist': {'existence': 'n.', 'existing': 'adj.'},
    'expand': {'expansion': 'n.', 'expanding': 'adj.'},
    'expect': {'expectation': 'n.', 'expected': 'adj.'},
    'explain': {'explanation': 'n.'},
    'exploit': {'exploitation': 'n.'},
    'explore': {'exploration': 'n.', 'exploratory': 'adj.'},
    'export': {'exportation': 'n.', 'exported': 'adj.'},
    'expose': {'exposure': 'n.', 'exposed': 'adj.'},
    'express': {'expression': 'n.', 'expressive': 'adj.'},
    'extend': {'extension': 'n.', 'extensive': 'adj.'},
    'extreme': {'extremely': 'adv.', 'extremity': 'n.'},
    'facilitate': {'facilitation': 'n.'},
    'familiar': {'familiarity': 'n.', 'familiarize': 'v.'},
    'fascinate': {'fascination': 'n.', 'fascinating': 'adj.'},
    'finance': {'financial': 'adj.', 'financially': 'adv.'},
    'flexible': {'flexibility': 'n.'},
    'focus': {'focused': 'adj.'},
    'fortunate': {'fortunately': 'adv.', 'unfortunately': 'adv.'},
    'found': {'foundation': 'n.', 'founder': 'n.'},
    'fragile': {'fragility': 'n.'},
    'frequent': {'frequency': 'n.', 'frequently': 'adv.'},
    'fulfill': {'fulfillment': 'n.', 'fulfilled': 'adj.'},
    'function': {'functional': 'adj.'},
    'generate': {'generation': 'n.', 'generator': 'n.'},
    'generous': {'generosity': 'n.'},
    'globe': {'global': 'adj.', 'globalization': 'n.'},
    'govern': {'government': 'n.', 'governing': 'adj.'},
    'graduate': {'graduation': 'n.', 'undergraduate': 'n.'},
    'guide': {'guidance': 'n.', 'guiding': 'adj.'},
    'harmony': {'harmonious': 'adj.'},
    'healthy': {'health': 'n.', 'healthier': 'adj.'},
    'hesitate': {'hesitation': 'n.', 'hesitant': 'adj.'},
    'identify': {'identification': 'n.', 'identity': 'n.'},
    'ignore': {'ignorance': 'n.', 'ignorant': 'adj.'},
    'illustrate': {'illustration': 'n.', 'illustrative': 'adj.'},
    'imagine': {'imagination': 'n.', 'imaginative': 'adj.'},
    'implement': {'implementation': 'n.'},
    'imply': {'implication': 'n.', 'implied': 'adj.'},
    'import': {'importation': 'n.', 'imported': 'adj.'},
    'impose': {'imposition': 'n.'},
    'impress': {'impression': 'n.', 'impressive': 'adj.'},
    'improve': {'improvement': 'n.', 'improved': 'adj.'},
    'indicate': {'indication': 'n.', 'indicative': 'adj.'},
    'individual': {'individually': 'adv.'},
    'industry': {'industrial': 'adj.', 'industrialize': 'v.'},
    'influence': {'influential': 'adj.'},
    'inform': {'information': 'n.', 'informative': 'adj.'},
    'inherit': {'inheritance': 'n.', 'inherited': 'adj.'},
    'innovate': {'innovation': 'n.', 'innovative': 'adj.'},
    'insist': {'insistence': 'n.', 'insistent': 'adj.'},
    'inspect': {'inspection': 'n.', 'inspector': 'n.'},
    'inspire': {'inspiration': 'n.', 'inspiring': 'adj.'},
    'install': {'installation': 'n.'},
    'instruct': {'instruction': 'n.', 'instructive': 'adj.'},
    'integrate': {'integration': 'n.', 'integrated': 'adj.'},
    'intelligent': {'intelligence': 'n.'},
    'intend': {'intention': 'n.', 'intended': 'adj.'},
    'intense': {'intensity': 'n.', 'intensely': 'adv.'},
    'interact': {'interaction': 'n.', 'interactive': 'adj.'},
    'interpret': {'interpretation': 'n.'},
    'intervene': {'intervention': 'n.'},
    'invest': {'investment': 'n.', 'investor': 'n.'},
    'investigate': {'investigation': 'n.'},
    'involve': {'involvement': 'n.', 'involved': 'adj.'},
    'isolate': {'isolation': 'n.', 'isolated': 'adj.'},
    'judge': {'judgment': 'n.', 'judicial': 'adj.'},
    'justify': {'justification': 'n.', 'justified': 'adj.'},
    'legal': {'legally': 'adv.'},
    'liberal': {'liberate': 'v.', 'liberation': 'n.'},
    'limit': {'limitation': 'n.', 'limited': 'adj.'},
    'locate': {'location': 'n.', 'located': 'adj.'},
    'logic': {'logical': 'adj.', 'logically': 'adv.'},
    'maintain': {'maintenance': 'n.'},
    'major': {'majority': 'n.'},
    'manage': {'management': 'n.', 'manager': 'n.'},
    'manufacture': {'manufacturing': 'n.', 'manufacturer': 'n.'},
    'measure': {'measurement': 'n.', 'measurable': 'adj.'},
    'memory': {'memorable': 'adj.', 'memorize': 'v.'},
    'migrate': {'migration': 'n.', 'immigrant': 'n.'},
    'modify': {'modification': 'n.'},
    'monitor': {'monitoring': 'n.'},
    'motivate': {'motivation': 'n.', 'motivated': 'adj.'},
    'mystery': {'mysterious': 'adj.'},
    'necessary': {'necessarily': 'adv.', 'necessity': 'n.'},
    'negotiate': {'negotiation': 'n.'},
    'normal': {'normally': 'adv.', 'normalize': 'v.'},
    'object': {'objection': 'n.', 'objective': 'adj.'},
    'observe': {'observation': 'n.'},
    'obtain': {'obtainable': 'adj.', 'obtained': 'adj.'},
    'occupy': {'occupation': 'n.', 'occupied': 'adj.'},
    'offend': {'offense': 'n.', 'offensive': 'adj.'},
    'operate': {'operation': 'n.', 'operational': 'adj.'},
    'oppose': {'opposition': 'n.', 'opposed': 'adj.'},
    'organize': {'organization': 'n.', 'organized': 'adj.'},
    'origin': {'original': 'adj.', 'originally': 'adv.'},
    'participate': {'participation': 'n.', 'participant': 'n.'},
    'patient': {'patience': 'n.', 'patiently': 'adv.'},
    'perceive': {'perception': 'n.', 'perceptive': 'adj.'},
    'perform': {'performance': 'n.', 'performer': 'n.'},
    'permit': {'permission': 'n.', 'permissible': 'adj.'},
    'persist': {'persistence': 'n.', 'persistent': 'adj.'},
    'persuade': {'persuasion': 'n.', 'persuasive': 'adj.'},
    'phenomenon': {'phenomenal': 'adj.'},
    'politics': {'political': 'adj.', 'politician': 'n.'},
    'pollute': {'pollution': 'n.', 'polluted': 'adj.'},
    'popular': {'popularity': 'n.'},
    'possess': {'possession': 'n.'},
    'possible': {'possibility': 'n.', 'possibly': 'adv.'},
    'predict': {'prediction': 'n.', 'predictable': 'adj.'},
    'prefer': {'preference': 'n.', 'preferable': 'adj.'},
    'prepare': {'preparation': 'n.', 'prepared': 'adj.'},
    'prescribe': {'prescription': 'n.'},
    'preserve': {'preservation': 'n.', 'preserved': 'adj.'},
    'prevent': {'prevention': 'n.', 'preventable': 'adj.'},
    'proceed': {'procedure': 'n.'},
    'produce': {'production': 'n.', 'productive': 'adj.'},
    'profession': {'professional': 'adj.'},
    'profit': {'profitable': 'adj.', 'profitability': 'n.'},
    'progress': {'progressive': 'adj.'},
    'prohibit': {'prohibition': 'n.', 'prohibited': 'adj.'},
    'promote': {'promotion': 'n.', 'promotional': 'adj.'},
    'propose': {'proposal': 'n.', 'proposed': 'adj.'},
    'protect': {'protection': 'n.', 'protective': 'adj.'},
    'prove': {'proof': 'n.', 'proven': 'adj.'},
    'provide': {'provision': 'n.', 'provided': 'conj.'},
    'publish': {'publication': 'n.', 'published': 'adj.'},
    'punish': {'punishment': 'n.'},
    'pursue': {'pursuit': 'n.'},
    'qualify': {'qualification': 'n.', 'qualified': 'adj.'},
    'react': {'reaction': 'n.', 'reactive': 'adj.'},
    'real': {'reality': 'n.', 'realistic': 'adj.'},
    'realize': {'realization': 'n.'},
    'receive': {'reception': 'n.', 'recipient': 'n.'},
    'recognize': {'recognition': 'n.', 'recognizable': 'adj.'},
    'recommend': {'recommendation': 'n.'},
    'recover': {'recovery': 'n.'},
    'reduce': {'reduction': 'n.', 'reduced': 'adj.'},
    'refer': {'reference': 'n.'},
    'reflect': {'reflection': 'n.', 'reflective': 'adj.'},
    'regard': {'regardless': 'adv.', 'regarding': 'prep.'},
    'register': {'registration': 'n.'},
    'regulate': {'regulation': 'n.', 'regulatory': 'adj.'},
    'reinforce': {'reinforcement': 'n.'},
    'reject': {'rejection': 'n.'},
    'relate': {'relation': 'n.', 'relationship': 'n.'},
    'reliable': {'reliability': 'n.'},
    'relieve': {'relief': 'n.', 'relieved': 'adj.'},
    'remain': {'remainder': 'n.', 'remaining': 'adj.'},
    'remove': {'removal': 'n.', 'removed': 'adj.'},
    'renew': {'renewal': 'n.', 'renewable': 'adj.'},
    'represent': {'representation': 'n.', 'representative': 'n.'},
    'require': {'requirement': 'n.', 'required': 'adj.'},
    'reserve': {'reservation': 'n.', 'reserved': 'adj.'},
    'resist': {'resistance': 'n.', 'resistant': 'adj.'},
    'resolve': {'resolution': 'n.', 'resolved': 'adj.'},
    'respond': {'response': 'n.', 'responsive': 'adj.'},
    'responsible': {'responsibility': 'n.'},
    'restore': {'restoration': 'n.'},
    'restrict': {'restriction': 'n.', 'restrictive': 'adj.'},
    'retain': {'retention': 'n.'},
    'retire': {'retirement': 'n.'},
    'reveal': {'revelation': 'n.'},
    'revise': {'revision': 'n.'},
    'revolution': {'revolutionary': 'adj.'},
    'satisfy': {'satisfaction': 'n.', 'satisfactory': 'adj.'},
    'secure': {'security': 'n.', 'secured': 'adj.'},
    'select': {'selection': 'n.', 'selective': 'adj.'},
    'sensitive': {'sensitivity': 'n.', 'sensible': 'adj.'},
    'separate': {'separation': 'n.', 'separately': 'adv.'},
    'signify': {'significant': 'adj.', 'significance': 'n.'},
    'similar': {'similarity': 'n.', 'similarly': 'adv.'},
    'simplify': {'simplification': 'n.', 'simplified': 'adj.'},
    'solve': {'solution': 'n.'},
    'special': {'specialize': 'v.', 'specialist': 'n.'},
    'specific': {'specifically': 'adv.', 'specify': 'v.'},
    'stable': {'stability': 'n.', 'stabilize': 'v.'},
    'stimulate': {'stimulation': 'n.', 'stimulating': 'adj.'},
    'strengthen': {'strength': 'n.'},
    'struggle': {'struggling': 'adj.'},
    'submit': {'submission': 'n.'},
    'succeed': {'success': 'n.', 'successful': 'adj.'},
    'sufficient': {'sufficiently': 'adv.', 'insufficient': 'adj.'},
    'suggest': {'suggestion': 'n.', 'suggestive': 'adj.'},
    'support': {'supportive': 'adj.', 'supporter': 'n.'},
    'survive': {'survival': 'n.', 'survivor': 'n.'},
    'suspect': {'suspicion': 'n.', 'suspicious': 'adj.'},
    'sustain': {'sustainable': 'adj.', 'sustainability': 'n.'},
    'symbol': {'symbolic': 'adj.', 'symbolize': 'v.'},
    'sympathy': {'sympathetic': 'adj.'},
    'technology': {'technological': 'adj.'},
    'tend': {'tendency': 'n.'},
    'tolerate': {'tolerance': 'n.', 'tolerable': 'adj.'},
    'tradition': {'traditional': 'adj.'},
    'transform': {'transformation': 'n.'},
    'translate': {'translation': 'n.', 'translator': 'n.'},
    'transmit': {'transmission': 'n.'},
    'treat': {'treatment': 'n.', 'treaty': 'n.'},
    'ultimate': {'ultimately': 'adv.'},
    'understand': {'understanding': 'n.', 'understandable': 'adj.'},
    'unique': {'uniquely': 'adv.', 'uniqueness': 'n.'},
    'urge': {'urgent': 'adj.', 'urgency': 'n.'},
    'valid': {'validity': 'n.', 'validate': 'v.'},
    'value': {'valuable': 'adj.', 'valuation': 'n.'},
    'vary': {'variety': 'n.', 'variation': 'n.', 'various': 'adj.'},
    'verify': {'verification': 'n.'},
    'violate': {'violation': 'n.', 'violent': 'adj.'},
    'volunteer': {'voluntary': 'adj.', 'voluntarily': 'adv.'},
    'warn': {'warning': 'n.'},
    'withdraw': {'withdrawal': 'n.'},
    'worth': {'worthy': 'adj.', 'worthwhile': 'adj.'},
    'yield': {'yielding': 'adj.', 'unyielding': 'adj.'},
}

REVERSE_DERIV = {}
for base, ders in DERIVATIVES.items():
    for der_word, der_pos in ders.items():
        if der_word not in REVERSE_DERIV:
            REVERSE_DERIV[der_word] = []
        REVERSE_DERIV[der_word].append({'base': base, 'base_pos': der_pos})

# ===== 短语映射表 =====
REAL_PHRASES = {
    'abandon': ['abandon ship', 'abandon hope', 'abandon oneself'],
    'absorb': ['absorb information', 'absorb the cost', 'be absorbed in'],
    'accelerate': ['accelerate growth', 'accelerate the pace'],
    'accumulate': ['accumulate wealth', 'accumulate experience'],
    'acknowledge': ['acknowledge receipt', 'acknowledge the fact'],
    'acquire': ['acquire knowledge', 'acquire a taste for'],
    'adapt': ['adapt to change', 'adapt oneself to'],
    'address': ['address the issue', 'address a letter'],
    'adjust': ['adjust to', 'adjust the settings'],
    'adopt': ['adopt a policy', 'adopt a child'],
    'affect': ['affect the outcome', 'deeply affected'],
    'allocate': ['allocate resources', 'allocate funds'],
    'analyze': ['analyze data', 'analyze the situation'],
    'apply': ['apply for', 'apply to', 'apply pressure'],
    'appreciate': ['appreciate art', 'appreciate the effort'],
    'approach': ['approach the problem', 'take an approach'],
    'approve': ['approve of', 'approve the plan'],
    'arrange': ['arrange a meeting', 'arrange for'],
    'assess': ['assess the damage', 'assess the risk'],
    'assign': ['assign blame', 'assign a task', 'assign responsibility'],
    'assist': ['assist with', 'assist in'],
    'assume': ['assume responsibility', 'assume the worst'],
    'attach': ['attach importance to', 'attach a file'],
    'attempt': ['attempt to do', 'make an attempt'],
    'attend': ['attend a meeting', 'attend to'],
    'attribute': ['attribute to', 'attribute the success'],
    'balance': ['balance work and life', 'strike a balance'],
    'bear': ['bear in mind', 'bear the burden', 'bear fruit'],
    'benefit': ['benefit from', 'mutual benefit'],
    'boost': ['boost the economy', 'boost morale'],
    'bound': ['bound to', 'be bound by', 'out of bounds'],
    'break': ['break down', 'break through', 'break up'],
    'bring': ['bring about', 'bring up', 'bring forward'],
    'capture': ['capture attention', 'capture the moment'],
    'carry': ['carry out', 'carry on', 'carry weight'],
    'cast': ['cast doubt on', 'cast a shadow', 'cast a vote'],
    'catch': ['catch up with', 'catch on', 'catch a glimpse'],
    'cause': ['cause and effect', 'cause trouble'],
    'challenge': ['challenge the status quo', 'face a challenge'],
    'change': ['change one\'s mind', 'change over time'],
    'charge': ['take charge of', 'free of charge', 'charge with'],
    'cheat': ['cheat sheet', 'cheat on', 'cheat death'],
    'check': ['check in', 'check out', 'check on'],
    'claim': ['claim responsibility', 'make a claim'],
    'collapse': ['collapse under pressure', 'economic collapse'],
    'combine': ['combine with', 'combine efforts'],
    'commit': ['commit to', 'commit a crime', 'commit oneself'],
    'communicate': ['communicate with', 'communicate effectively'],
    'compare': ['compare with', 'compare to', 'beyond compare'],
    'compete': ['compete with', 'compete for'],
    'complain': ['complain about', 'complain of'],
    'complete': ['complete the task', 'complete works'],
    'concentrate': ['concentrate on', 'concentrate efforts'],
    'concern': ['concern about', 'show concern for'],
    'confirm': ['confirm the reservation', 'confirm that'],
    'conflict': ['conflict with', 'in conflict', 'conflict of interest'],
    'confront': ['confront the issue', 'be confronted with'],
    'connect': ['connect with', 'connect to', 'stay connected'],
    'consider': ['consider doing', 'consider the possibility'],
    'consist': ['consist of', 'consist in'],
    'construct': ['construct a theory', 'construct a building'],
    'consume': ['consume resources', 'consume time'],
    'contain': ['contain the spread', 'contain oneself'],
    'contribute': ['contribute to', 'make a contribution'],
    'control': ['take control of', 'under control', 'out of control'],
    'convert': ['convert to', 'convert into'],
    'convey': ['convey a message', 'convey the meaning'],
    'convince': ['convince of', 'convince to do'],
    'cope': ['cope with', 'cope with stress'],
    'correspond': ['correspond to', 'correspond with'],
    'count': ['count on', 'count down', 'count for'],
    'cover': ['cover up', 'cover the cost', 'cover a topic'],
    'create': ['create opportunities', 'create problems'],
    'deal': ['deal with', 'a great deal of', 'close the deal'],
    'debate': ['debate on', 'a heated debate'],
    'decide': ['decide on', 'decide whether to'],
    'declare': ['declare war', 'declare independence'],
    'decline': ['decline an invitation', 'in decline'],
    'define': ['define as', 'define the boundaries'],
    'deliver': ['deliver a speech', 'deliver goods', 'deliver results'],
    'demand': ['demand for', 'in demand', 'meet the demand'],
    'demonstrate': ['demonstrate the ability', 'demonstrate against'],
    'deny': ['deny doing', 'deny the charge'],
    'depend': ['depend on', 'it depends'],
    'describe': ['describe as', 'describe in detail'],
    'deserve': ['deserve attention', 'deserve the blame'],
    'design': ['design for', 'by design', 'design a system'],
    'determine': ['determine to do', 'determine the cause'],
    'develop': ['develop skills', 'develop a plan'],
    'devote': ['devote to', 'devote oneself to'],
    'differ': ['differ from', 'differ in', 'beg to differ'],
    'direct': ['direct attention to', 'take direct action'],
    'discover': ['discover the truth', 'discover new lands'],
    'discuss': ['discuss with', 'discuss the matter'],
    'dismiss': ['dismiss the idea', 'dismiss from'],
    'display': ['on display', 'display the results'],
    'dispose': ['dispose of', 'dispose waste'],
    'distinguish': ['distinguish between', 'distinguish from'],
    'distribute': ['distribute to', 'distribute leaflets'],
    'divide': ['divide into', 'divide by', 'digital divide'],
    'dominate': ['dominate the market', 'dominate the conversation'],
    'doubt': ['doubt about', 'without doubt', 'cast doubt on'],
    'draw': ['draw attention to', 'draw a conclusion', 'draw on'],
    'drop': ['drop out of', 'drop by', 'drop the idea'],
    'earn': ['earn a living', 'earn respect', 'earn interest'],
    'effect': ['take effect', 'have an effect on', 'in effect'],
    'eliminate': ['eliminate poverty', 'eliminate the possibility'],
    'emerge': ['emerge from', 'emerge as'],
    'emphasize': ['emphasize the importance'],
    'employ': ['employ a method', 'employ workers'],
    'enable': ['enable to do', 'enable access'],
    'encounter': ['encounter difficulties', 'a chance encounter'],
    'encourage': ['encourage to do', 'encourage innovation'],
    'engage': ['engage in', 'engage with', 'be engaged to'],
    'enhance': ['enhance performance', 'enhance the quality'],
    'ensure': ['ensure that', 'ensure safety'],
    'establish': ['establish a relationship', 'establish rules'],
    'evaluate': ['evaluate the performance', 'evaluate the data'],
    'evolve': ['evolve from', 'evolve into', 'evolve over time'],
    'examine': ['examine the evidence', 'examine carefully'],
    'exceed': ['exceed expectations', 'exceed the limit'],
    'exchange': ['exchange ideas', 'in exchange for', 'exchange rate'],
    'exclude': ['exclude from', 'exclude the possibility'],
    'exercise': ['exercise regularly', 'exercise one\'s right'],
    'exist': ['exist in', 'cease to exist'],
    'expand': ['expand business', 'expand one\'s horizons'],
    'expect': ['expect to do', 'expect the unexpected'],
    'experience': ['gain experience', 'first-hand experience'],
    'explain': ['explain to', 'explain the reason'],
    'exploit': ['exploit resources', 'exploit the weakness'],
    'explore': ['explore the possibility', 'explore new frontiers'],
    'expose': ['expose to', 'expose the truth', 'be exposed to'],
    'express': ['express oneself', 'express concern'],
    'extend': ['extend the deadline', 'extend a warm welcome'],
    'face': ['face a challenge', 'face to face', 'in the face of'],
    'facilitate': ['facilitate communication', 'facilitate the process'],
    'fail': ['fail to do', 'fail the test', 'without fail'],
    'fall': ['fall behind', 'fall into', 'fall apart'],
    'favor': ['in favor of', 'do a favor'],
    'figure': ['figure out', 'a public figure', 'figure of speech'],
    'focus': ['focus on', 'bring into focus', 'out of focus'],
    'follow': ['follow up', 'follow the rules', 'as follows'],
    'force': ['force to do', 'in force', 'come into force'],
    'fulfill': ['fulfill a dream', 'fulfill the requirements'],
    'gain': ['gain access to', 'gain experience', 'gain weight'],
    'generate': ['generate revenue', 'generate interest'],
    'grant': ['take for granted', 'grant a request'],
    'guard': ['guard against', 'on guard', 'off guard'],
    'handle': ['handle the situation', 'handle with care'],
    'hold': ['hold on', 'hold a meeting', 'hold true'],
    'identify': ['identify with', 'identify the problem'],
    'impact': ['impact on', 'have an impact on'],
    'implement': ['implement a plan', 'implement changes'],
    'imply': ['imply that', 'as the name implies'],
    'impose': ['impose on', 'impose restrictions'],
    'impress': ['impress on', 'impress with', 'be impressed by'],
    'improve': ['improve on', 'improve the quality'],
    'increase': ['increase by', 'increase in', 'on the increase'],
    'indicate': ['indicate that', 'indicate the direction'],
    'influence': ['influence on', 'under the influence'],
    'inform': ['inform of', 'inform about', 'keep informed'],
    'insist': ['insist on', 'insist that'],
    'integrate': ['integrate into', 'integrate with'],
    'intend': ['intend to do', 'intend for', 'as intended'],
    'interact': ['interact with', 'interact socially'],
    'interpret': ['interpret as', 'interpret the data'],
    'introduce': ['introduce to', 'introduce a new policy'],
    'invest': ['invest in', 'invest time and effort'],
    'investigate': ['investigate the case', 'investigate further'],
    'involve': ['involve in', 'get involved with', 'involve doing'],
    'keep': ['keep in mind', 'keep up with', 'keep on doing'],
    'lack': ['lack of', 'lack the ability', 'for lack of'],
    'launch': ['launch a campaign', 'launch into'],
    'lead': ['lead to', 'lead by example', 'take the lead'],
    'limit': ['limit to', 'time limit', 'off limits'],
    'maintain': ['maintain order', 'maintain relationships'],
    'manage': ['manage to do', 'manage a business'],
    'manufacture': ['manufacture goods', 'manufacturing industry'],
    'measure': ['measure up to', 'take measures'],
    'merge': ['merge with', 'merge into', 'merge companies'],
    'monitor': ['monitor progress', 'monitor closely'],
    'motivate': ['motivate to do', 'keep motivated'],
    'negotiate': ['negotiate with', 'negotiate a deal'],
    'obtain': ['obtain from', 'obtain permission'],
    'offer': ['offer to do', 'make an offer', 'on offer'],
    'operate': ['operate on', 'operate a machine'],
    'oppose': ['oppose to', 'as opposed to', 'oppose the plan'],
    'organize': ['organize an event', 'organize data'],
    'overcome': ['overcome difficulties', 'overcome fear'],
    'participate': ['participate in', 'participate actively'],
    'pass': ['pass away', 'pass on', 'pass the test'],
    'perform': ['perform well', 'perform a task'],
    'persist': ['persist in', 'if symptoms persist'],
    'persuade': ['persuade to do', 'persuade of'],
    'point': ['point out', 'point of view', 'to the point'],
    'pose': ['pose a threat', 'pose a question'],
    'predict': ['predict the future', 'predict accurately'],
    'prefer': ['prefer to', 'prefer over', 'would prefer'],
    'prepare': ['prepare for', 'prepare to do', 'be prepared'],
    'present': ['present a report', 'at present'],
    'preserve': ['preserve the environment', 'preserve food'],
    'prevent': ['prevent from', 'prevent the spread'],
    'proceed': ['proceed with', 'proceed to do'],
    'produce': ['produce results', 'produce goods'],
    'promote': ['promote to', 'promote health'],
    'propose': ['propose a plan', 'propose to do'],
    'protect': ['protect from', 'protect against'],
    'prove': ['prove to be', 'prove one\'s point'],
    'provide': ['provide with', 'provide for'],
    'pursue': ['pursue a career', 'pursue happiness'],
    'put': ['put forward', 'put up with', 'put into practice'],
    'qualify': ['qualify for', 'qualify as'],
    'raise': ['raise awareness', 'raise funds', 'raise a question'],
    'range': ['range from', 'a wide range of'],
    'reach': ['reach a conclusion', 'reach out to', 'within reach'],
    'react': ['react to', 'react against'],
    'realize': ['realize the importance', 'realize a dream'],
    'receive': ['receive attention', 'receive treatment'],
    'recognize': ['recognize as', 'recognize the importance'],
    'recover': ['recover from', 'recover consciousness'],
    'reduce': ['reduce to', 'reduce the risk', 'reduce costs'],
    'refer': ['refer to', 'refer to as'],
    'reflect': ['reflect on', 'reflect the reality'],
    'refuse': ['refuse to do', 'refuse point-blank'],
    'regard': ['regard as', 'with regard to', 'in this regard'],
    'relate': ['relate to', 'be related to'],
    'release': ['release from', 'press release'],
    'relieve': ['relieve stress', 'relieve pain', 'relieve of'],
    'rely': ['rely on', 'rely heavily on'],
    'remain': ['remain to be seen', 'remain silent', 'remain loyal'],
    'remove': ['remove from', 'remove obstacles'],
    'replace': ['replace with', 'replace by'],
    'represent': ['represent the interests of'],
    'require': ['require that', 'require attention'],
    'resolve': ['resolve the issue', 'resolve to do'],
    'respond': ['respond to', 'respond quickly'],
    'restore': ['restore order', 'restore confidence'],
    'restrict': ['restrict to', 'restrict access'],
    'result': ['result in', 'result from', 'as a result'],
    'retain': ['retain control', 'retain information'],
    'reveal': ['reveal the truth', 'reveal oneself'],
    'reverse': ['reverse the trend', 'in reverse'],
    'rise': ['give rise to', 'rise to the challenge', 'on the rise'],
    'risk': ['at risk', 'take a risk', 'risk doing'],
    'rule': ['rule out', 'as a rule', 'rule over'],
    'run': ['run into', 'run out of', 'in the long run'],
    'seek': ['seek out', 'seek to do', 'seek help'],
    'sense': ['make sense', 'a sense of', 'common sense'],
    'separate': ['separate from', 'separate into'],
    'serve': ['serve as', 'serve the purpose'],
    'set': ['set up', 'set out to do', 'set an example'],
    'settle': ['settle down', 'settle for', 'settle a dispute'],
    'share': ['share with', 'fair share', 'market share'],
    'shed': ['shed light on', 'shed tears'],
    'shift': ['shift from', 'shift the blame'],
    'show': ['show off', 'show up', 'show concern'],
    'sign': ['sign up for', 'sign a contract'],
    'solve': ['solve the problem', 'solve a mystery'],
    'sort': ['sort out', 'sort of', 'of all sorts'],
    'spark': ['spark a debate', 'spark outrage'],
    'spend': ['spend on', 'spend time doing', 'spend money'],
    'spread': ['spread out', 'spread the word'],
    'stand': ['stand out', 'stand for', 'stand by'],
    'stimulate': ['stimulate growth', 'stimulate the economy'],
    'strengthen': ['strengthen ties', 'strengthen the position'],
    'stress': ['stress the importance', 'under stress'],
    'struggle': ['struggle with', 'struggle for', 'struggle to do'],
    'submit': ['submit to', 'submit a report'],
    'succeed': ['succeed in', 'succeed to the throne'],
    'suffer': ['suffer from', 'suffer losses'],
    'suggest': ['suggest that', 'suggest doing'],
    'support': ['support for', 'in support of'],
    'suppose': ['be supposed to', 'suppose that'],
    'survive': ['survive on', 'survive the accident'],
    'suspect': ['suspect of', 'suspect that'],
    'sustain': ['sustain damage', 'sustain growth', 'sustain life'],
    'tackle': ['tackle the problem', 'tackle the issue'],
    'tend': ['tend to do', 'tend to be', 'tend towards'],
    'think': ['think about', 'think over', 'think highly of'],
    'trace': ['trace back to', 'without a trace'],
    'track': ['keep track of', 'on the right track', 'track down'],
    'transfer': ['transfer to', 'transfer funds'],
    'transform': ['transform into', 'transform the industry'],
    'treat': ['treat as', 'treat with respect'],
    'trigger': ['trigger a reaction', 'trigger the alarm'],
    'trust': ['trust in', 'trust with', 'build trust'],
    'turn': ['turn out', 'turn down', 'in turn'],
    'undergo': ['undergo changes', 'undergo surgery'],
    'undermine': ['undermine authority', 'undermine confidence'],
    'undertake': ['undertake a task', 'undertake to do'],
    'urge': ['urge to do', 'urge that', 'urge caution'],
    'vary': ['vary from', 'vary widely', 'vary in'],
    'verify': ['verify the information', 'verify the identity'],
    'view': ['view as', 'point of view', 'in view of'],
    'violate': ['violate the law', 'violate rights'],
    'vote': ['vote for', 'vote against', 'cast a vote'],
    'warn': ['warn of', 'warn against', 'warn that'],
    'weigh': ['weigh the pros and cons', 'weigh on'],
    'withdraw': ['withdraw from', 'withdraw money'],
    'work': ['work out', 'work on', 'work for'],
    'yield': ['yield to', 'yield results', 'high yield'],
}

def make_good_hints(meaning, word, pos):
    hints = []
    if len(meaning) >= 4: hints.append(f"首两字是「{meaning[0]}{meaning[1]}…」")
    elif len(meaning) >= 2: hints.append(f"首字为「{meaning[0]}」")
    if pos:
        for k, v in {'n.': '名词', 'v.': '动词', 'adj.': '形容词', 'adv.': '副词'}.items():
            if pos.startswith(k): hints.append(f"这是一个{v}"); break
    opposites = {'大': '小', '小': '大', '高': '低', '低': '高', '多': '少', '少': '多', '好': '坏', '坏': '好',
                 '快': '慢', '慢': '快', '新': '旧', '旧': '新', '强': '弱', '弱': '强', '真': '假', '假': '真'}
    for ch, opp in opposites.items():
        if ch in meaning: hints.append(f"试着从「{opp}」的反面来想"); break
    if len(hints) < 2: hints.append(f"回忆'{word}'的相关含义")
    return hints[:4]

# ===== Build WORD_BANK JS =====
bank = 'const WORD_BANK = [\n'
for wi, w in enumerate(words_list):
    pos_str = w['pos'] if w['pos'] else 'n./v./adj.'
    meanings = w['meanings'][:6]
    phonetic = '/' + re.sub(r'[^a-z]', '', w['word']) + '/'
    word_lower = w['word'].lower()
    first_meaning = meanings[0] if meanings else ''
    
    # ---- Segment 1: 原词 - only first meaning accepted (fix: was meanings[:3]) ----
    segs = [{
        'text': w['word'],
        'label': '原词',
        'answer': [meanings[0]] if meanings else ['?'],
        'hints': make_good_hints(first_meaning, w['word'], pos_str),
    }]
    
    # ---- Segment 2: 同根词 or 词义2 ----
    derivatives = DERIVATIVES.get(word_lower)
    seg2_answer = [meanings[1]] if len(meanings) > 1 else ([meanings[0]] if meanings else ['?'])
    seg2_target_meaning = meanings[1] if len(meanings) > 1 else first_meaning
    
    if derivatives:
        der_word = list(derivatives.keys())[0]
        der_pos = derivatives[der_word]
        segs.append({
            'text': der_word,
            'label': f'同根词({der_pos})',
            'answer': seg2_answer,
            'hints': [f"「{w['word']}」→「{der_word}」词性变为{der_pos}"] + make_good_hints(seg2_target_meaning, w['word'], pos_str)[:3],
        })
    elif word_lower in REVERSE_DERIV:
        rev = REVERSE_DERIV[word_lower][0]
        segs.append({
            'text': rev['base'],
            'label': '同根词(原形)',
            'answer': seg2_answer,
            'hints': [f"「{w['word']}」来自「{rev['base']}」"] + make_good_hints(seg2_target_meaning, w['word'], pos_str)[:3],
        })
    else:
        # No real derivative — use word itself with different meaning
        seg2_label = '词义2' if len(meanings) > 1 else '用法'
        segs.append({
            'text': w['word'],
            'label': seg2_label,
            'answer': seg2_answer,
            'hints': make_good_hints(seg2_target_meaning, w['word'], pos_str),
        })
    
    # ---- Segment 3: 短语 or 词义3 ----
    phrase_candidates = REAL_PHRASES.get(word_lower)
    seg3_answer = [meanings[2]] if len(meanings) > 2 else ([meanings[1]] if len(meanings) > 1 else ([meanings[0]] if meanings else ['?']))
    seg3_target_meaning = meanings[2] if len(meanings) > 2 else (meanings[1] if len(meanings) > 1 else first_meaning)
    
    if phrase_candidates:
        chosen_phrase = phrase_candidates[hash(w['word']) % len(phrase_candidates)]
        segs.append({
            'text': chosen_phrase,
            'label': '短语',
            'answer': seg3_answer,
            'hints': [f"「{w['word']}」的常见搭配"] + make_good_hints(seg3_target_meaning, w['word'], pos_str)[:3],
        })
    elif len(meanings) > 2:
        segs.append({
            'text': w['word'],
            'label': '词义3',
            'answer': seg3_answer,
            'hints': make_good_hints(seg3_target_meaning, w['word'], pos_str),
        })
    else:
        # Fallback phrase
        prep = ['of', 'to', 'for', 'with', 'in', 'on', 'from'][hash(w['word']) % 7]
        if pos_str and 'v.' in pos_str:
            fallback_phrase = f"{w['word']} {prep}"
        elif pos_str and 'n.' in pos_str:
            fallback_phrase = f"{w['word']} of"
        elif pos_str and 'adj.' in pos_str:
            fallback_phrase = f"be {w['word']} {prep}"
        else:
            fallback_phrase = f"{w['word']} {prep}"
        segs.append({
            'text': fallback_phrase,
            'label': '短语',
            'answer': seg3_answer,
            'hints': [f"「{w['word']}」的常见搭配"] + make_good_hints(seg3_target_meaning, w['word'], pos_str)[:3],
        })
    
    bank += '  {'
    bank += f'word:"{w["word"]}",phonetic:"{phonetic}",pos:"{pos_str}",segments:['
    
    for si, seg in enumerate(segs):
        seg_json = json.dumps(seg, ensure_ascii=False)
        bank += seg_json
        if si < len(segs) - 1:
            bank += ','
    
    bank += ']}'
    if wi < len(words_list) - 1:
        bank += ','
    bank += '\n'

bank += '];\n\n'

# Insert into HTML
with open(os.path.join(d, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = 'const WORD_BANK = ['
start_idx = html.find(start_marker)
end_marker = "// ==================== 名句宝库"
end_idx = html.find(end_marker)
close_idx = html.rfind('];', start_idx, end_idx)

if start_idx == -1 or close_idx == -1:
    print("ERROR: markers not found")
    exit(1)

new_html = html[:start_idx] + bank + html[close_idx+2:]

out_path = os.path.join(d, 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

size_kb = os.path.getsize(out_path) / 1024
print(f"Wrote {size_kb:.0f} KB, {len(words_list)} words")
print("Done!")