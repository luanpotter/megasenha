import httplib2
from pyquery import PyQuery

def is_ban(w):
    return {
        'símb.': True,
        'pref.': True,
        'suf.': True,
        'contr.': True,
        'interj.': True,
        'sigla': True,
        'elem.': True,
    }.get(w, False)

def is_ban2(w):
    return {
        'conj.': True,
        'prep.': True,
        'det.': True,
        'art.': True,
    }.get(w, False)

def process_word(w):
	resp, content = httplib2.Http().request('https://www.priberam.pt/dlpo/' + w)
	if 'Palavra n\\xc3\\xa3o encontrada.' not in str(content):
		pq = PyQuery(content)

		tags = [i for i in pq.items('span.varpt')]
		words = []
		for tag in tags:
			children = tag.children()
			if (children.size() == 1 and children.eq(0).is_('b') and children.eq(0).children().size() == 0):
				words.append(tag)
			#print(tag)
			#print(children.size())
			#print(children.eq(0).is_('b'))
			#print(children.eq(0).children().size())
		
		word = None
		category = None
		for w in words:
			word_parents = w.parents()
			c = word_parents.eq(word_parents.size() - 1).find('em').eq(0).text().split(' ')[0]
			if (is_ban2(c)):
				return None
			if (not is_ban(c) and word == None and category == None):
				word = w
				category = c

		if (word == None or category == None):
			return None
		else:
			return word.text() + ' ' + category
	else:
		return None
	#array = [i.val('class') for i in pq.items('span')]

words = []

with open('megasenha.db', 'w') as wfile:
	with open('palavras', 'r') as rfile:
		i = 0
		for line in rfile:
			word = process_word(line.rstrip())
			i += 1
			if word != None:
				wfile.write(word + '\n')
				print(str(i) + ' ' + word)
			else:
				print(i)
			
			
