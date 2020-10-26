import spacy

class SWrapper:
	'''
	A class to encapsulate all functionalities that can be exploited from spacy linguistics
	'''
	def __init__(self, inp_sent='', disable=list()):
		'''
		Initializing inp sentence inside constructor
		'''

		# Loading model and processing sentence
		self.en_nlp = spacy.load('en', disable=disable)
		self.set_sent(inp_sent)

	def __str__(self):
		'''
		prints this object
		'''
		return self._inp_sent

	def get_sent(self):
		'''
		get class property sentence back
		'''
		return self._inp_sent

	def set_sent(self, inp_sent):
		'''
		set class property sentence
		'''
		self._inp_sent = inp_sent
		self.doc = self.en_nlp(inp_sent)

	def get_pos(self):
		'''
		returns superficial pos tags as [[word, tag]...]
		'''
		pos = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.pos_)
			pos.append(temp)

		return pos

	def get_lemmas(self):
		'''
		returns a list of tokens in the sentence in their basic form
		'''
		lemmas = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.lemma_)
			lemmas.append(temp)

		return lemmas

	def get_entities(self):
		'''
		returns list of tags with thier entity labesl as [[word, label]...]
		'''
		labels = list()
		for token in self.doc.ents:
			temp = list()
			temp.append(token.text)
			temp.append(token.label_)
			labels.append(temp)

		return labels

	def get_noun_chunks(self):
		'''
		returns all noun phrases
		'''
		return list(self.doc.noun_chunks)

	def get_some_tags(self, patterns=list()):
		'''
		returns all tokens with tags recognized
		'''
		tokens = list()
		tags = self.get_tags()

		if type(patterns) != list:
			raise Exception('Please send pos tag patterns in a list !!')

		# Checking each element of patterns against tags
		for tag in tags:
			if any(pattern in tag[1] for pattern in patterns):
				tokens.append(tag[0])

		return tokens

	def get_tags(self):
		'''
		returns detailed pos tags as [[word, tag]...]
		'''
		tag = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.tag_)
			tag.append(temp)

		return tag

	def get_dependency(self):
		'''
		Returns dependency in format [[relation, governor, dependent]...]
		'''
		dependencies = list()
		for token in self.doc:
			temp = list()
			temp.append(token.dep_)	# adding relation
			temp.append(token.head.text) # adding governor/head
			temp.append(token.text) # adding dependent
			dependencies.append(temp)

		return dependencies

	def is_alpha(self):
		'''
		returns if word is alpha numeric or not [[word, is_alpha]...]
		'''
		is_alpha = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.is_alpha)
			is_alpha.append(temp)

		return is_alpha

	def is_stop(self):
		'''
		returns if word is stop word or not [[word, is_stop]...]
		'''
		is_stop = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.is_stop)
			is_stop.append(temp)

		return is_stop

if __name__ == '__main__':
	inp_sent = input('Enter Input Sentence for Dependency Parsing : \n >> ')

	spacy_obj = SWrapper(inp_sent)
	# print (spacy_obj)
	# print (spacy_obj.get_dependency())
	# print (spacy_obj.get_entities())
	# print (spacy_obj.get_noun_chunks())
	# print (spacy_obj.get_some_tags(patterns=['NN']))
	# print (spacy_obj.get_pos())
	# print (spacy_obj.get_tags())
	# print (spacy_obj.get_lemmas())
	# print (spacy_obj.is_alpha())
	# print (spacy_obj.is_stop())