from module import XMPPModule

# rough count of number of syllables in a given word
def sylcnt(word):
	lastvowel = False
	syl = 0
	for i in range(len(word)):
		c = word[i]
		vowel = (c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u')
		if lastvowel != vowel and (c != 'e' or i != len(word) - 1):
			syl += 1
	if syl == 0:
		syl = 1
	return syl

# filters non-alphanumeric characters and lowercases everything
def clean(x):
	y = ''
	for i in range(len(x)):
		if x[i].isalpha():
			y += x[i]
	return y.lower()

# This function determines is a string can be split into lines deterministic of a given structure
# Returns false if it cannot be so, the stanza of poem if it can
def haiku(line, counts):
	words = filter(lambda w: len(w) > 0, line.split(' '))
	i = 0
	cnt = 0
	stanza = [[]]

	for w in words:
		if i >= len(counts):
			return False

		w = clean(w)

		if len(w) > 0:
			cnt += sylcnt(w)
			stanza[i].append(w)

			if cnt == counts[i]:
				i += 1
				cnt = 0
				stanza.append([])
			elif cnt > counts[i]:
				return False

	if i == len(counts):
		stanza.pop()
		return stanza
	return False

# makes a string from a stanza
def make_poem(stanza):
	formed = ''
	for line in stanza:
		first = True
		for word in line:
			if first:
				formed += word[0].upper() + word[1:]
				first = False
			else:
				formed += ' ' + word
		formed += '\n'
	return formed

class Haiku(XMPPModule):
	def handleMessage(self, msg):
		if 'haiku' in self.xmpp.config.keys():
			forms = self.xmpp.config['haiku']['forms']
		else:
			forms = [{
				'name': 'haiku',
				'form': [5, 7, 5]
			}, {
				'name': 'tanka',
				'form': [5, 7, 5, 7, 7]
			}]

		for pair in forms:
			name = pair['name']
			form = pair['form']
			s = haiku(msg['body'], form)
			if s:
				reply = make_poem(s)
				reply = msg['from'].bare + ', I proffer that your prose is a poem, a ' + name + ':\n' + reply
				self.xmpp.reply(msg, reply)

