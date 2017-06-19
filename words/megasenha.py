import httplib2
from time import sleep
from pyquery import PyQuery
from joblib import Parallel, delayed

def is_ban_weak(w):
    return {
        'símb.': True,
        'pref.': True,
        'suf.': True,
        'contr.': True,
        'sigla': True,
        'elem.': True,
        'abrev.': True,
    }.get(w, False)

def is_ban_strong(w):
    return {
        'conj.': True,
        'prep.': True,
        'det.': True,
        'art.': True,
        'interj.': True,
        'pron.': True,
    }.get(w, False)

def process_word(w):
	w = w.lower()
	if (len(w) < 2) or (' ' in w) or ('-' in w):
		return ('', '')
	while True:
		try:
			resp, content = httplib2.Http().request('https://www.priberam.pt/dlpo/' + w)
			break
		except Exception:
			sleep(0.5)
	if 'Palavra n\\xc3\\xa3o encontrada.' not in str(content):
		pq = PyQuery(content)

		tags = [i for i in pq.items('span.varpb')]
		words = []
		for tag in tags:
			children = tag.children()
			if (children.size() == 1) and children.eq(0).is_('b') and (children.eq(0).children().size() == 0):
				words.append(tag)

		wordsEquals = []
		wordsSimilar = []

		for w0 in words:
			if (' ' in w0.text()) or ('-' in w0.text()):
				continue
			elif w0.text() == w:
				wordsEquals.append(w0)
			else:
				wordsSimilar.append(w0)
		words = wordsEquals + wordsSimilar
		
		word = None
		category = None
		for w0 in words:
			word_parents = w0.parents()
			cs = word_parents.eq(word_parents.size() - 1).find('em')
			for i in range(0, cs.size()):
				c = cs.eq(i).text().split(' ')[0]
				if is_ban_strong(c):
					return ('', '')
				if (not is_ban_weak(c)) and (word == None) and (category == None):
					word = w0.text()
					category = c

		if (word == None) or (category == None):
			return ('', '')
		else:
			word = word.lower()
			print(word + ' ' + category)
			return (word, category)
	else:
		return ('', '')

lines = []

with open('palavras', 'r') as rfile:
	for line in rfile:
		lines.append(line.rstrip())

words = dict(Parallel(n_jobs=300)(delayed(process_word)(line) for line in lines))

files = ['numerais', 'pronomes', 'cidades', 'paises', 'pessoas']
for f0 in files:
	with open(f0, 'r') as rfile:
		for line in rfile:
			aux = line.rstrip().lower().split(' ')
			word = aux[0]
			category = aux[1]
			words[word] = category
words['balotar'] = 'v.'

with open('megasenha.db', 'w') as wfile:
	for word, category in sorted(words.items()):
		if (word != '') and (category != ''):
			wfile.write(word + ' ' + category + '\n')
			
