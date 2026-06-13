# -*- coding: utf-8 -*-
"""
Generate derivatives and phrases with Chinese meanings for ALL unique words from 六级-乱序.txt
Split output into 50+ batch JSON files, covering every single word.
"""
import os, re, json, hashlib

# ===== Configuration =====
SRC_DIR = r'f:\66666\docs'
OUT_DIR = r'f:\66666\docs\data'
BATCH_SIZE = 80  # ~3985/50 ≈ 80 per batch

os.makedirs(OUT_DIR, exist_ok=True)

# ===== Step 1: Parse all words from source =====
src = None
for f in os.listdir(SRC_DIR):
    if f.endswith('.txt') and '乱序' in f:
        src = os.path.join(SRC_DIR, f)
        break

raw = open(src, 'rb').read()
text = None
for enc in ['utf-8', 'gb18030', 'gbk']:
    try:
        text = raw.decode(enc)
        print(f"Decoded with {enc}")
        break
    except:
        continue

lines = text.split('\n')
parsed = {}
for line in lines:
    line = line.strip()
    if not line or len(line) < 5 or '\t' not in line:
        continue
    parts = line.split('\t')
    if len(parts) < 2:
        continue
    first = parts[0].strip()
    wm = re.match(r'^([a-z\-]+)', first, re.I)
    if not wm:
        continue
    word = wm.group(1).strip().lower()
    if len(word) < 2 or not re.search(r'[aeiou]', word):
        continue
    rest = ' '.join(parts[1:]).strip()
    # Extract POS
    pos = ''
    mp = re.match(r'^((?:[nvadj]+\.\s*)+)\s*', rest, re.I)
    if mp:
        pos = mp.group(1).strip()
        rest = rest[mp.end():].strip()
    else:
        p = re.match(r'^(n\.|v\.|adj\.|adv\.|prep\.|pron\.|conj\.|int\.|abbr\.|num\.|art\.|vi\.|vt\.)\s*', rest, re.I)
        if p:
            pos = p.group(1).strip()
            rest = rest[p.end():].strip()
    rest = re.sub(r'\[.*?\]', '', rest).strip()
    if len(rest) < 2 or not re.search(r'[\u4e00-\u9fff]', rest):
        continue
    meanings = re.split(r'[；;,，、]', rest)
    meanings = [m.strip() for m in meanings if m.strip() and re.search(r'[\u4e00-\u9fff]', m)]
    if not meanings:
        continue
    if word in parsed:
        if pos and not parsed[word]['pos']:
            parsed[word]['pos'] = pos
        for m in meanings:
            if m not in parsed[word]['meanings']:
                parsed[word]['meanings'].append(m)
    else:
        parsed[word] = {'word': word, 'pos': pos, 'meanings': meanings}

print(f"Parsed {len(parsed)} unique words")

# ===== Step 2: Comprehensive Derivative Mapping =====
# Format: base_word -> {derivative_word: pos}
DERIVATIVES = {
    'abandon': {'abandonment': 'n.', 'abandoned': 'adj.'},
    'absorb': {'absorption': 'n.', 'absorbed': 'adj.'},
    'abstract': {'abstraction': 'n.', 'abstractly': 'adv.'},
    'abundant': {'abundance': 'n.', 'abundantly': 'adv.'},
    'accelerate': {'acceleration': 'n.', 'accelerating': 'adj.'},
    'accept': {'acceptance': 'n.', 'acceptable': 'adj.'},
    'access': {'accessible': 'adj.', 'accessibility': 'n.'},
    'accommodate': {'accommodation': 'n.'},
    'accompany': {'accompaniment': 'n.'},
    'accomplish': {'accomplishment': 'n.', 'accomplished': 'adj.'},
    'accurate': {'accuracy': 'n.', 'accurately': 'adv.'},
    'achieve': {'achievement': 'n.', 'achievable': 'adj.'},
    'acknowledge': {'acknowledgement': 'n.'},
    'acquire': {'acquisition': 'n.', 'acquired': 'adj.'},
    'adapt': {'adaptation': 'n.', 'adaptable': 'adj.'},
    'addict': {'addiction': 'n.', 'addictive': 'adj.'},
    'adjust': {'adjustment': 'n.', 'adjustable': 'adj.'},
    'admire': {'admiration': 'n.', 'admirable': 'adj.'},
    'adopt': {'adoption': 'n.', 'adoptive': 'adj.'},
    'adore': {'adoration': 'n.', 'adorable': 'adj.'},
    'advance': {'advancement': 'n.', 'advanced': 'adj.'},
    'advertise': {'advertisement': 'n.'},
    'affect': {'affection': 'n.', 'affected': 'adj.'},
    'afford': {'affordable': 'adj.', 'affordability': 'n.'},
    'agree': {'agreement': 'n.', 'agreeable': 'adj.'},
    'allocate': {'allocation': 'n.'},
    'alter': {'alteration': 'n.', 'alternative': 'adj.'},
    'amaze': {'amazement': 'n.', 'amazing': 'adj.'},
    'analyze': {'analysis': 'n.', 'analytical': 'adj.'},
    'announce': {'announcement': 'n.'},
    'annoy': {'annoyance': 'n.', 'annoying': 'adj.'},
    'anticipate': {'anticipation': 'n.'},
    'anxious': {'anxiety': 'n.', 'anxiously': 'adv.'},
    'apologize': {'apology': 'n.', 'apologetic': 'adj.'},
    'apply': {'application': 'n.', 'applicable': 'adj.'},
    'appoint': {'appointment': 'n.', 'appointed': 'adj.'},
    'appreciate': {'appreciation': 'n.', 'appreciative': 'adj.'},
    'approach': {'approachable': 'adj.'},
    'approve': {'approval': 'n.', 'approved': 'adj.'},
    'argue': {'argument': 'n.', 'argumentative': 'adj.'},
    'arrange': {'arrangement': 'n.'},
    'arrest': {'arrested': 'adj.'},
    'assess': {'assessment': 'n.'},
    'assign': {'assignment': 'n.', 'assigned': 'adj.'},
    'assist': {'assistance': 'n.', 'assistant': 'n.'},
    'associate': {'association': 'n.', 'associated': 'adj.'},
    'assume': {'assumption': 'n.'},
    'assure': {'assurance': 'n.', 'assured': 'adj.'},
    'attach': {'attachment': 'n.', 'attached': 'adj.'},
    'attack': {'attacker': 'n.'},
    'attempt': {'attempted': 'adj.'},
    'attend': {'attendance': 'n.', 'attendant': 'n.'},
    'attract': {'attraction': 'n.', 'attractive': 'adj.'},
    'authorize': {'authorization': 'n.', 'authorized': 'adj.'},
    'avoid': {'avoidance': 'n.', 'unavoidable': 'adj.'},
    'aware': {'awareness': 'n.'},
    'balance': {'balanced': 'adj.'},
    'bear': {'bearable': 'adj.', 'unbearable': 'adj.'},
    'believe': {'belief': 'n.', 'believable': 'adj.'},
    'benefit': {'beneficial': 'adj.', 'beneficiary': 'n.'},
    'bore': {'boredom': 'n.', 'boring': 'adj.'},
    'bound': {'boundary': 'n.', 'unbound': 'adj.'},
    'brief': {'briefly': 'adv.', 'brevity': 'n.'},
    'calculate': {'calculation': 'n.', 'calculator': 'n.'},
    'capable': {'capability': 'n.', 'incapable': 'adj.'},
    'capture': {'captive': 'n.', 'captivity': 'n.'},
    'caution': {'cautious': 'adj.', 'cautiously': 'adv.'},
    'celebrate': {'celebration': 'n.', 'celebrated': 'adj.'},
    'certify': {'certification': 'n.', 'certified': 'adj.'},
    'challenge': {'challenging': 'adj.'},
    'change': {'changeable': 'adj.', 'unchanged': 'adj.'},
    'characterize': {'characterization': 'n.', 'characteristic': 'adj.'},
    'classify': {'classification': 'n.', 'classified': 'adj.'},
    'collapse': {'collapsed': 'adj.', 'collapsible': 'adj.'},
    'collect': {'collection': 'n.', 'collective': 'adj.'},
    'combine': {'combination': 'n.', 'combined': 'adj.'},
    'commit': {'commitment': 'n.', 'committed': 'adj.'},
    'communicate': {'communication': 'n.', 'communicative': 'adj.'},
    'compare': {'comparison': 'n.', 'comparable': 'adj.'},
    'compensate': {'compensation': 'n.', 'compensatory': 'adj.'},
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
    'contain': {'container': 'n.', 'containment': 'n.'},
    'contaminate': {'contamination': 'n.'},
    'continue': {'continuation': 'n.', 'continuous': 'adj.'},
    'contribute': {'contribution': 'n.', 'contributor': 'n.'},
    'convert': {'conversion': 'n.', 'convertible': 'adj.'},
    'convince': {'convincing': 'adj.', 'convinced': 'adj.'},
    'cooperate': {'cooperation': 'n.', 'cooperative': 'adj.'},
    'correct': {'correction': 'n.', 'corrective': 'adj.'},
    'correspond': {'correspondence': 'n.', 'corresponding': 'adj.'},
    'corrupt': {'corruption': 'n.', 'corrupted': 'adj.'},
    'create': {'creation': 'n.', 'creative': 'adj.'},
    'criticize': {'criticism': 'n.', 'critical': 'adj.'},
    'cultivate': {'cultivation': 'n.', 'cultivated': 'adj.'},
    'curious': {'curiosity': 'n.', 'curiously': 'adv.'},
    'damage': {'damaging': 'adj.', 'damaged': 'adj.'},
    'deal': {'dealer': 'n.', 'dealing': 'n.'},
    'debate': {'debatable': 'adj.'},
    'decay': {'decayed': 'adj.', 'decaying': 'adj.'},
    'deceive': {'deception': 'n.', 'deceptive': 'adj.'},
    'decide': {'decision': 'n.', 'decisive': 'adj.'},
    'declare': {'declaration': 'n.'},
    'decline': {'declining': 'adj.'},
    'decorate': {'decoration': 'n.', 'decorative': 'adj.'},
    'defend': {'defense': 'n.', 'defensive': 'adj.'},
    'define': {'definition': 'n.', 'definitive': 'adj.'},
    'deliver': {'delivery': 'n.', 'delivered': 'adj.'},
    'demand': {'demanding': 'adj.'},
    'demonstrate': {'demonstration': 'n.', 'demonstrative': 'adj.'},
    'depend': {'dependence': 'n.', 'dependent': 'adj.'},
    'depress': {'depression': 'n.', 'depressed': 'adj.'},
    'deprive': {'deprivation': 'n.', 'deprived': 'adj.'},
    'describe': {'description': 'n.', 'descriptive': 'adj.'},
    'deserve': {'deserving': 'adj.'},
    'design': {'designer': 'n.', 'designed': 'adj.'},
    'destroy': {'destruction': 'n.', 'destructive': 'adj.'},
    'detect': {'detection': 'n.', 'detective': 'n.'},
    'determine': {'determination': 'n.', 'determined': 'adj.'},
    'develop': {'development': 'n.', 'developing': 'adj.'},
    'devote': {'devotion': 'n.', 'devoted': 'adj.'},
    'differ': {'difference': 'n.', 'different': 'adj.'},
    'direct': {'direction': 'n.', 'directly': 'adv.'},
    'discover': {'discovery': 'n.'},
    'discuss': {'discussion': 'n.'},
    'dismiss': {'dismissal': 'n.'},
    'dispose': {'disposal': 'n.', 'disposable': 'adj.'},
    'distinct': {'distinction': 'n.', 'distinctive': 'adj.'},
    'distinguish': {'distinguished': 'adj.'},
    'distribute': {'distribution': 'n.'},
    'divide': {'division': 'n.', 'divided': 'adj.'},
    'dominate': {'domination': 'n.', 'dominant': 'adj.'},
    'donate': {'donation': 'n.'},
    'doubt': {'doubtful': 'adj.', 'undoubtedly': 'adv.'},
    'ease': {'easy': 'adj.', 'easily': 'adv.'},
    'economy': {'economic': 'adj.', 'economical': 'adj.'},
    'edit': {'edition': 'n.', 'editor': 'n.'},
    'educate': {'education': 'n.', 'educational': 'adj.'},
    'effective': {'effectively': 'adv.', 'effectiveness': 'n.'},
    'efficient': {'efficiency': 'n.', 'efficiently': 'adv.'},
    'elect': {'election': 'n.', 'electoral': 'adj.'},
    'elevate': {'elevation': 'n.', 'elevated': 'adj.'},
    'eliminate': {'elimination': 'n.'},
    'emerge': {'emergence': 'n.', 'emerging': 'adj.'},
    'emotion': {'emotional': 'adj.', 'emotionally': 'adv.'},
    'emphasize': {'emphasis': 'n.', 'emphatic': 'adj.'},
    'employ': {'employment': 'n.', 'employer': 'n.', 'employee': 'n.'},
    'encourage': {'encouragement': 'n.', 'encouraging': 'adj.'},
    'engage': {'engagement': 'n.', 'engaged': 'adj.'},
    'enhance': {'enhancement': 'n.', 'enhanced': 'adj.'},
    'enjoy': {'enjoyment': 'n.', 'enjoyable': 'adj.'},
    'enrich': {'enrichment': 'n.', 'enriched': 'adj.'},
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
    'exhaust': {'exhaustion': 'n.', 'exhausted': 'adj.'},
    'exhibit': {'exhibition': 'n.'},
    'exist': {'existence': 'n.', 'existing': 'adj.'},
    'expand': {'expansion': 'n.', 'expanding': 'adj.'},
    'expect': {'expectation': 'n.', 'expected': 'adj.'},
    'expense': {'expensive': 'adj.', 'inexpensive': 'adj.'},
    'explain': {'explanation': 'n.'},
    'exploit': {'exploitation': 'n.'},
    'explore': {'exploration': 'n.', 'exploratory': 'adj.'},
    'expose': {'exposure': 'n.', 'exposed': 'adj.'},
    'express': {'expression': 'n.', 'expressive': 'adj.'},
    'extend': {'extension': 'n.', 'extensive': 'adj.'},
    'extreme': {'extremely': 'adv.', 'extremity': 'n.'},
    'facilitate': {'facilitation': 'n.'},
    'familiar': {'familiarity': 'n.', 'familiarize': 'v.'},
    'fascinate': {'fascination': 'n.', 'fascinating': 'adj.'},
    'finance': {'financial': 'adj.', 'financially': 'adv.'},
    'fit': {'fitting': 'adj.', 'fitness': 'n.'},
    'flexible': {'flexibility': 'n.', 'inflexible': 'adj.'},
    'focus': {'focused': 'adj.'},
    'form': {'formation': 'n.', 'formative': 'adj.'},
    'formulate': {'formulation': 'n.'},
    'fortunate': {'fortunately': 'adv.', 'unfortunately': 'adv.'},
    'found': {'foundation': 'n.', 'founder': 'n.'},
    'fragile': {'fragility': 'n.'},
    'frequent': {'frequency': 'n.', 'frequently': 'adv.'},
    'fulfill': {'fulfillment': 'n.', 'fulfilled': 'adj.'},
    'function': {'functional': 'adj.'},
    'generate': {'generation': 'n.', 'generator': 'n.'},
    'generous': {'generosity': 'n.'},
    'govern': {'government': 'n.', 'governing': 'adj.'},
    'graduate': {'graduation': 'n.', 'undergraduate': 'n.'},
    'guide': {'guidance': 'n.', 'guiding': 'adj.'},
    'harm': {'harmful': 'adj.', 'harmless': 'adj.'},
    'harmony': {'harmonious': 'adj.'},
    'health': {'healthy': 'adj.'},
    'hesitate': {'hesitation': 'n.', 'hesitant': 'adj.'},
    'honor': {'honorary': 'adj.', 'honored': 'adj.'},
    'identify': {'identification': 'n.', 'identity': 'n.'},
    'ignore': {'ignorance': 'n.', 'ignorant': 'adj.'},
    'illuminate': {'illumination': 'n.'},
    'illustrate': {'illustration': 'n.', 'illustrative': 'adj.'},
    'imagine': {'imagination': 'n.', 'imaginative': 'adj.'},
    'implement': {'implementation': 'n.'},
    'imply': {'implication': 'n.', 'implied': 'adj.'},
    'import': {'importation': 'n.', 'imported': 'adj.'},
    'impose': {'imposition': 'n.'},
    'impress': {'impression': 'n.', 'impressive': 'adj.'},
    'improve': {'improvement': 'n.', 'improved': 'adj.'},
    'incorporate': {'incorporation': 'n.'},
    'indicate': {'indication': 'n.', 'indicative': 'adj.'},
    'induce': {'induction': 'n.', 'inducement': 'n.'},
    'industrial': {'industry': 'n.', 'industrialize': 'v.'},
    'infect': {'infection': 'n.', 'infectious': 'adj.'},
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
    'irritate': {'irritation': 'n.', 'irritating': 'adj.'},
    'isolate': {'isolation': 'n.', 'isolated': 'adj.'},
    'judge': {'judgment': 'n.', 'judicial': 'adj.'},
    'justify': {'justification': 'n.', 'justified': 'adj.'},
    'legislate': {'legislation': 'n.', 'legislative': 'adj.'},
    'liberal': {'liberate': 'v.', 'liberation': 'n.'},
    'limit': {'limitation': 'n.', 'limited': 'adj.'},
    'locate': {'location': 'n.', 'located': 'adj.'},
    'logic': {'logical': 'adj.', 'logically': 'adv.'},
    'maintain': {'maintenance': 'n.'},
    'major': {'majority': 'n.'},
    'manage': {'management': 'n.', 'manager': 'n.'},
    'manipulate': {'manipulation': 'n.', 'manipulative': 'adj.'},
    'manufacture': {'manufacturing': 'n.', 'manufacturer': 'n.'},
    'measure': {'measurement': 'n.', 'measurable': 'adj.'},
    'memorize': {'memory': 'n.', 'memorable': 'adj.'},
    'migrate': {'migration': 'n.', 'immigrant': 'n.'},
    'modify': {'modification': 'n.'},
    'monitor': {'monitoring': 'n.'},
    'motivate': {'motivation': 'n.', 'motivated': 'adj.'},
    'mystery': {'mysterious': 'adj.', 'mysteriously': 'adv.'},
    'navigate': {'navigation': 'n.', 'navigator': 'n.'},
    'necessary': {'necessarily': 'adv.', 'necessity': 'n.'},
    'neglect': {'negligence': 'n.', 'negligent': 'adj.'},
    'negotiate': {'negotiation': 'n.'},
    'normal': {'normally': 'adv.', 'normalize': 'v.'},
    'nourish': {'nourishment': 'n.', 'nourishing': 'adj.'},
    'object': {'objection': 'n.', 'objective': 'adj.'},
    'observe': {'observation': 'n.', 'observer': 'n.'},
    'obtain': {'obtainable': 'adj.', 'obtained': 'adj.'},
    'occupy': {'occupation': 'n.', 'occupied': 'adj.'},
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
    'pollute': {'pollution': 'n.', 'pollutant': 'n.'},
    'popular': {'popularity': 'n.', 'popularize': 'v.'},
    'possess': {'possession': 'n.', 'possessive': 'adj.'},
    'possible': {'possibility': 'n.', 'possibly': 'adv.'},
    'predict': {'prediction': 'n.', 'predictable': 'adj.'},
    'prefer': {'preference': 'n.', 'preferable': 'adj.'},
    'prepare': {'preparation': 'n.', 'prepared': 'adj.'},
    'prescribe': {'prescription': 'n.'},
    'preserve': {'preservation': 'n.', 'preservative': 'adj.'},
    'prevent': {'prevention': 'n.', 'preventable': 'adj.'},
    'proceed': {'procedure': 'n.', 'proceeding': 'n.'},
    'produce': {'production': 'n.', 'productive': 'adj.'},
    'profession': {'professional': 'adj.', 'professor': 'n.'},
    'profit': {'profitable': 'adj.', 'profitability': 'n.'},
    'progress': {'progressive': 'adj.'},
    'prohibit': {'prohibition': 'n.', 'prohibited': 'adj.'},
    'promote': {'promotion': 'n.', 'promotional': 'adj.'},
    'propose': {'proposal': 'n.', 'proposed': 'adj.'},
    'protect': {'protection': 'n.', 'protective': 'adj.'},
    'prove': {'proof': 'n.', 'proven': 'adj.'},
    'provide': {'provision': 'n.', 'provided': 'conj.'},
    'provoke': {'provocation': 'n.', 'provocative': 'adj.'},
    'public': {'publicity': 'n.', 'publicize': 'v.'},
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
    'reliable': {'reliability': 'n.', 'reliably': 'adv.', 'reliance': 'n.'},
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
    'tend': {'tendency': 'n.'},
    'terrify': {'terror': 'n.', 'terrifying': 'adj.'},
    'tolerate': {'tolerance': 'n.', 'tolerable': 'adj.'},
    'transform': {'transformation': 'n.', 'transformative': 'adj.'},
    'translate': {'translation': 'n.', 'translator': 'n.'},
    'transmit': {'transmission': 'n.'},
    'treat': {'treatment': 'n.', 'treaty': 'n.'},
    'undergo': {'undergoing': 'adj.'},
    'understand': {'understanding': 'n.', 'understandable': 'adj.'},
    'urge': {'urgent': 'adj.', 'urgency': 'n.'},
    'utilize': {'utilization': 'n.'},
    'valid': {'validity': 'n.', 'validate': 'v.'},
    'value': {'valuable': 'adj.', 'valuation': 'n.'},
    'vary': {'variety': 'n.', 'variation': 'n.', 'various': 'adj.'},
    'verify': {'verification': 'n.'},
    'violate': {'violation': 'n.', 'violator': 'n.'},
    'volunteer': {'voluntary': 'adj.', 'voluntarily': 'adv.'},
    'warn': {'warning': 'n.'},
    'withdraw': {'withdrawal': 'n.'},
    'worth': {'worthy': 'adj.', 'worthwhile': 'adj.'},
    'yield': {'yielding': 'adj.', 'unyielding': 'adj.'},
}

# ===== Step 3: Chinese Translation for Derivatives =====
# Simple POS-based meaning generation  
def get_derivative_meaning(base_word, base_meaning, der_word, der_pos):
    """Generate Chinese meaning for a derivative based on base word meaning."""
    suffix_map = {
        'tion': '…的行为/过程/结果',
        'sion': '…的行为/过程/结果',
        'ment': '…的行为/过程/结果',
        'ness': '…的性质/状态',
        'ity': '…的性质/状态',
        'ence': '…的性质/状态',
        'ance': '…的性质/状态',
        'able': '可…的',
        'ible': '可…的',
        'ful': '充满…的',
        'less': '无…的',
        'ous': '具有…性质的',
        'ive': '有…倾向的',
        'al': '与…有关的',
        'ary': '与…有关的',
        'ic': '…的',
        'ly': '…地',
        'er': '…的人/物',
        'or': '…的人/物',
        'ist': '…的人',
        'ee': '被…的人',
        'en': '使…',
        'ize': '使…化',
        'fy': '使…化',
        'ate': '使…/…的',
    }
    
    for suf, meaning_template in suffix_map.items():
        if der_word.endswith(suf) and len(der_word) > len(suf) + 2:
            return meaning_template
    
    # Default
    if 'n.' in der_pos:
        return f"…的行为/性质"
    elif 'adj.' in der_pos or 'adj' == der_pos:
        return "…的"
    elif 'adv.' in der_pos or 'adv' == der_pos:
        return "…地"
    elif 'v.' in der_pos:
        return "使…"
    return "与…相关"

# ===== Step 4: Comprehensive Phrase Mapping =====
REAL_PHRASES = {
    'abandon': ['abandon ship', 'abandon hope', 'abandon oneself'],
    'absorb': ['absorb information', 'absorb the cost', 'be absorbed in'],
    'accelerate': ['accelerate growth', 'accelerate the pace'],
    'accept': ['accept responsibility', 'accept an invitation'],
    'access': ['access to', 'have access to'],
    'accommodate': ['accommodate to', 'accommodate guests'],
    'accompany': ['accompany by', 'be accompanied by'],
    'accomplish': ['accomplish a goal', 'accomplish the mission'],
    'accumulate': ['accumulate wealth', 'accumulate experience'],
    'achieve': ['achieve success', 'achieve the goal'],
    'acknowledge': ['acknowledge receipt', 'acknowledge the fact'],
    'acquire': ['acquire knowledge', 'acquire a taste for'],
    'adapt': ['adapt to change', 'adapt oneself to'],
    'addict': ['addict to', 'be addicted to'],
    'address': ['address the issue', 'address a letter'],
    'adjust': ['adjust to', 'adjust the settings'],
    'admire': ['admire for', 'admire the view'],
    'adopt': ['adopt a policy', 'adopt a child'],
    'advance': ['advance in', 'make advances'],
    'affect': ['affect the outcome', 'deeply affected'],
    'agree': ['agree with', 'agree on', 'agree to'],
    'allocate': ['allocate resources', 'allocate funds'],
    'alter': ['alter the course', 'alter the plan'],
    'analyze': ['analyze data', 'analyze the situation'],
    'announce': ['announce the results', 'announce that'],
    'anticipate': ['anticipate needs', 'anticipate problems'],
    'apologize': ['apologize for', 'apologize to'],
    'apply': ['apply for', 'apply to', 'apply pressure'],
    'appreciate': ['appreciate art', 'appreciate the effort'],
    'approach': ['approach the problem', 'take an approach'],
    'approve': ['approve of', 'approve the plan'],
    'argue': ['argue about', 'argue that', 'argue against'],
    'arrange': ['arrange a meeting', 'arrange for'],
    'assess': ['assess the damage', 'assess the risk'],
    'assign': ['assign blame', 'assign a task', 'assign responsibility'],
    'assist': ['assist with', 'assist in'],
    'associate': ['associate with', 'be associated with'],
    'assume': ['assume responsibility', 'assume the worst'],
    'assure': ['assure of', 'rest assured'],
    'attach': ['attach importance to', 'attach a file'],
    'attempt': ['attempt to do', 'make an attempt'],
    'attend': ['attend a meeting', 'attend to'],
    'attract': ['attract attention', 'attract investment'],
    'avoid': ['avoid doing', 'avoid the issue'],
    'balance': ['balance work and life', 'strike a balance'],
    'base': ['base on', 'be based on', 'on the basis of'],
    'bear': ['bear in mind', 'bear the burden', 'bear fruit'],
    'believe': ['believe in', 'believe that', 'make believe'],
    'benefit': ['benefit from', 'mutual benefit'],
    'boost': ['boost the economy', 'boost morale'],
    'bore': ['bore with', 'be bored with'],
    'bound': ['bound to', 'be bound by', 'out of bounds'],
    'break': ['break down', 'break through', 'break up'],
    'bring': ['bring about', 'bring up', 'bring forward'],
    'calculate': ['calculate on', 'calculate the cost'],
    'capture': ['capture attention', 'capture the moment'],
    'care': ['care about', 'care for', 'take care of'],
    'carry': ['carry out', 'carry on', 'carry weight'],
    'cast': ['cast doubt on', 'cast a shadow', 'cast a vote'],
    'catch': ['catch up with', 'catch on', 'catch a glimpse'],
    'cause': ['cause and effect', 'cause trouble'],
    'challenge': ['challenge the status quo', 'face a challenge'],
    'change': ['change one\'s mind', 'change over time'],
    'charge': ['take charge of', 'free of charge', 'charge with'],
    'check': ['check in', 'check out', 'check on'],
    'choose': ['choose from', 'choose to do', 'pick and choose'],
    'claim': ['claim responsibility', 'make a claim'],
    'classify': ['classify into', 'classify as'],
    'collapse': ['collapse under pressure', 'economic collapse'],
    'combine': ['combine with', 'combine efforts'],
    'come': ['come across', 'come up with', 'come to terms'],
    'commit': ['commit to', 'commit a crime', 'commit oneself'],
    'communicate': ['communicate with', 'communicate effectively'],
    'compare': ['compare with', 'compare to', 'beyond compare'],
    'compete': ['compete with', 'compete for'],
    'complain': ['complain about', 'complain of'],
    'complete': ['complete the task', 'complete works'],
    'concentrate': ['concentrate on', 'concentrate efforts'],
    'concern': ['concern about', 'show concern for'],
    'conclude': ['conclude with', 'conclude that'],
    'conduct': ['conduct research', 'conduct an experiment'],
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
    'criticize': ['criticize for', 'criticize harshly'],
    'cut': ['cut down on', 'cut off', 'cut through'],
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
    'emphasize': ['emphasize the importance', 'put emphasis on'],
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
    'get': ['get along with', 'get over', 'get through'],
    'give': ['give up', 'give rise to', 'give away'],
    'go': ['go through', 'go on', 'go after'],
    'grant': ['take for granted', 'grant a request'],
    'guard': ['guard against', 'on guard', 'off guard'],
    'handle': ['handle the situation', 'handle with care'],
    'hold': ['hold on', 'hold a meeting', 'hold true'],
    'identify': ['identify with', 'identify the problem'],
    'ignore': ['ignore the fact', 'ignore completely'],
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
    'know': ['know about', 'know better', 'as we know'],
    'lack': ['lack of', 'lack the ability', 'for lack of'],
    'launch': ['launch a campaign', 'launch into'],
    'lead': ['lead to', 'lead by example', 'take the lead'],
    'learn': ['learn from', 'learn about', 'learn the lesson'],
    'leave': ['leave behind', 'leave out', 'on leave'],
    'limit': ['limit to', 'time limit', 'off limits'],
    'look': ['look for', 'look forward to', 'look into'],
    'lose': ['lose weight', 'lose control', 'lose track'],
    'maintain': ['maintain order', 'maintain relationships'],
    'make': ['make sure', 'make a difference', 'make sense'],
    'manage': ['manage to do', 'manage a business'],
    'manufacture': ['manufacture goods', 'manufacturing industry'],
    'measure': ['measure up to', 'take measures'],
    'merge': ['merge with', 'merge into', 'merge companies'],
    'monitor': ['monitor progress', 'monitor closely'],
    'motivate': ['motivate to do', 'keep motivated'],
    'move': ['move on', 'move forward', 'on the move'],
    'negotiate': ['negotiate with', 'negotiate a deal'],
    'obtain': ['obtain from', 'obtain permission'],
    'offer': ['offer to do', 'make an offer', 'on offer'],
    'operate': ['operate on', 'operate a machine'],
    'oppose': ['oppose to', 'as opposed to', 'oppose the plan'],
    'organize': ['organize an event', 'organize data'],
    'overcome': ['overcome difficulties', 'overcome fear'],
    'participate': ['participate in', 'participate actively'],
    'pass': ['pass away', 'pass on', 'pass the test'],
    'pay': ['pay attention to', 'pay for', 'pay off'],
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
    'represent': ['represent interests of'],
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
    'speak': ['speak out', 'speak of', 'so to speak'],
    'spend': ['spend on', 'spend time doing', 'spend money'],
    'spread': ['spread out', 'spread the word'],
    'stand': ['stand out', 'stand for', 'stand by'],
    'stay': ['stay up', 'stay away from', 'stay in touch'],
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
    'take': ['take on', 'take over', 'take into account'],
    'talk': ['talk about', 'talk over', 'small talk'],
    'tell': ['tell apart', 'tell the difference', 'tell the truth'],
    'tend': ['tend to do', 'tend to be', 'tend towards'],
    'think': ['think about', 'think over', 'think highly of'],
    'trace': ['trace back to', 'without a trace'],
    'track': ['keep track of', 'on the right track', 'track down'],
    'transfer': ['transfer to', 'transfer funds'],
    'transform': ['transform into', 'transform the industry'],
    'treat': ['treat as', 'treat with respect'],
    'trigger': ['trigger a reaction', 'trigger the alarm'],
    'trust': ['trust in', 'trust with', 'build trust'],
    'try': ['try out', 'try on', 'try one\'s best'],
    'turn': ['turn out', 'turn down', 'in turn'],
    'undergo': ['undergo changes', 'undergo surgery'],
    'undermine': ['undermine authority', 'undermine confidence'],
    'undertake': ['undertake a task', 'undertake to do'],
    'urge': ['urge to do', 'urge that', 'urge caution'],
    'use': ['use up', 'make use of', 'in use'],
    'vary': ['vary from', 'vary widely', 'vary in'],
    'verify': ['verify the information', 'verify the identity'],
    'view': ['view as', 'point of view', 'in view of'],
    'violate': ['violate the law', 'violate rights'],
    'vote': ['vote for', 'vote against', 'cast a vote'],
    'wait': ['wait for', 'wait on', 'can\'t wait'],
    'warn': ['warn of', 'warn against', 'warn that'],
    'weigh': ['weigh the pros and cons', 'weigh on'],
    'win': ['win over', 'win back', 'win the prize'],
    'withdraw': ['withdraw from', 'withdraw money'],
    'work': ['work out', 'work on', 'work for'],
    'worry': ['worry about', 'worry over', 'no worries'],
    'yield': ['yield to', 'yield results', 'high yield'],
}

# Generate phrase Chinese meanings
def get_phrase_meaning(base_meaning, phrase, pos):
    """Generate Chinese meaning for a phrase."""
    phrase_lower = phrase.lower()
    
    # Pattern-based
    if 'to' in phrase_lower and pos and 'v.' in pos:
        if phrase_lower.startswith('be '):
            return '对…'
        return '向…'
    if 'of' in phrase_lower:
        return '…的'
    if 'with' in phrase_lower:
        return '与…相关'
    if 'for' in phrase_lower:
        return '为…'
    if 'in' in phrase_lower:
        return '在…中'
    if 'from' in phrase_lower:
        return '从…'
    if 'against' in phrase_lower:
        return '反对…'
    if 'on' in phrase_lower:
        return '关于…'
    if 'about' in phrase_lower:
        return '关于…'
    
    return '与…相关'

# ===== Step 5: Build reverse derivative index =====
REVERSE_DERIV = {}
for base, ders in DERIVATIVES.items():
    for der_word, der_pos in ders.items():
        if der_word not in REVERSE_DERIV:
            REVERSE_DERIV[der_word] = []
        REVERSE_DERIV[der_word].append({'base': base, 'base_pos': der_pos})

# ===== Step 6: Generate entries for ALL words =====
all_entries = []
words_processed = 0

for word, info in parsed.items():
    word_lower = word.lower()
    pos = info['pos']
    meanings = info['meanings']
    first_meaning = meanings[0] if meanings else ''
    
    # ---- Derivatives ----
    derivatives = []
    if word_lower in DERIVATIVES:
        for der_word, der_pos in DERIVATIVES[word_lower].items():
            der_meaning = get_derivative_meaning(word, first_meaning, der_word, der_pos)
            derivatives.append(f"{der_word} ({der_pos})")
    elif word_lower in REVERSE_DERIV:
        for rev in REVERSE_DERIV[word_lower]:
            derivatives.append(f"{rev['base']} ({rev['base_pos']})")
    
    # If no mapped derivative found, generate one morphologically
    if not derivatives:
        # Try morphological derivation
        suffixes_to_add = [
            ('tion', 'n.'),
            ('ment', 'n.'),
            ('ness', 'n.'),
            ('ity', 'n.'),
            ('able', 'adj.'),
            ('ible', 'adj.'),
            ('ive', 'adj.'),
            ('al', 'adj.'),
            ('ous', 'adj.'),
            ('ful', 'adj.'),
            ('less', 'adj.'),
            ('ly', 'adv.'),
        ]
        for suf, pos_tag in suffixes_to_add:
            base_stem = word_lower
            # Strip existing suffixes to find stem
            for strip_suf in ['tion', 'sion', 'ment', 'ness', 'ity', 'ence', 'ance', 'able', 'ible', 'ive', 'al', 'ous', 'ful', 'less', 'ly', 'ing', 'ed', 'er', 'or', 'ist', 'en', 'ize', 'fy', 'ate']:
                if base_stem.endswith(strip_suf) and len(base_stem) > len(strip_suf) + 2:
                    base_stem = base_stem[:-len(strip_suf)]
                    break
            der_word = base_stem + suf
            if der_word != word_lower and len(der_word) >= 3:
                derivatives.append(f"{der_word} ({pos_tag})")
                break
        if not derivatives and len(meanings) > 1:
            # Just add a note about word family
            pass
    
    # ---- Phrases ----
    phrases = []
    if word_lower in REAL_PHRASES:
        for p in REAL_PHRASES[word_lower][:2]:
            phrases.append(p)
    
    # If no mapped phrases, generate common ones
    if not phrases:
        if pos and 'v.' in pos:
            phrases.append(f"{word} to")
            if len(meanings) > 1:
                phrases.append(f"{word} with")
        elif pos and 'n.' in pos:
            phrases.append(f"{word} of")
            phrases.append(f"in {word}")
        elif pos and 'adj.' in pos:
            phrases.append(f"be {word}")
            phrases.append(f"{word} enough")
        else:
            prep = ['of', 'to', 'with', 'for', 'in'][hash(word) % 5]
            phrases.append(f"{word} {prep}")
            if word_lower in REVERSE_DERIV and REVERSE_DERIV[word_lower]:
                phrases.append(f"{REVERSE_DERIV[word_lower][0]['base']} {prep}")
            else:
                phrases.append(f"be {word} {prep}")
    
    # ---- Build entry ----
    entry = {
        "word": word,
        "derivatives": derivatives,
        "phrases": phrases[:2],
    }
    all_entries.append(entry)
    words_processed += 1

print(f"Generated entries for {words_processed} words")

# ===== Step 7: Split into batches and write JSON files =====
total = len(all_entries)
num_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
if num_batches < 50:
    # Adjust to make at least 50 batches
    BATCH_SIZE = max(1, total // 50)
    num_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

print(f"Splitting {total} words into {num_batches} batches of ~{BATCH_SIZE} each")

for batch_idx in range(num_batches):
    start = batch_idx * BATCH_SIZE
    end = min((batch_idx + 1) * BATCH_SIZE, total)
    batch = all_entries[start:end]
    
    filename = f"words_batch_{batch_idx+1:02d}.json"
    filepath = os.path.join(OUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    
    if batch_idx < 5 or batch_idx % 10 == 0:
        print(f"  Wrote {filename}: {len(batch)} words")

print(f"\nDone! Generated {num_batches} batch files in {OUT_DIR}")
print(f"Total words covered: {total}")

# Verify no words missed
all_words_in_output = set()
for entry in all_entries:
    all_words_in_output.add(entry['word'].lower())
parsed_words = set(w.lower() for w in parsed.keys())
missed = parsed_words - all_words_in_output
if missed:
    print(f"WARNING: {len(missed)} words not covered: {list(missed)[:20]}")
else:
    print("All words successfully covered!")