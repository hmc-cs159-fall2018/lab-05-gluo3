from EditDistance import EditDistanceFinder
from LanguageModel import LanguageModel
import spacy

class SpellChecker():

	def __init__(self, channel_model=None, language_model=None, max_distance):
		self.channel_model = channel_model
		self.language_model = language_model
		self.max_distance = max_distance

	def load_channel_model(self, fp):
		self.channel_model = EditDistanceFinder()
		self.channel_model.train(fp)

	def load_language_model(self, fp):
		self.language_model = LanguageModel()
		self.language_model.load(fp)

	def bigram_score(self, prev_word, focus_word, next_word):
		return (self.language_model.bigram_score(prev_word,focus_word) + self.language_model.bigram_score(focus_word,next_word))/2

	def unigram_score(self, word):
		return self.language_model.unigram_score(word):

	def cm_score(self, error_word, corrected_word):
		return self.channel_model.align(error_word,corrected_word)[0]

	@staticmethod
	def isSubstring(w1, w2):
		for letter in w1:
			try:
				w2 = w2[w2.index(letter):]
			except:
				return False
		return True

	def inserts(self, word):
		output = []
		for w in self.language_model:
			if len(w) == len(word) + 1:
				if isSubstring(word, w):
					output.append(w)
		return output

	def deletes(self, word):
		output = []
		for w in self.language_model:
			if len(w) == len(word) - 1:
				if isSubstring(w,word):
					output.append(w)
		return output

	def substitutions(self, word):
		output = []
		for w in self.language_model:
			if len(w) == len(word):
				numInc = 0
				for i in range(len(w)):
					if w[i] != word[i]:
						numInc += 1
				if numInc == 1:
					output.append(w)
		return output

	def generate_candidates(self, word):
		output = [word]
		for _ in range(self.max_distance):
			newOutput = []
			for w in output:
				newOutput += self.inserts(word) + self.deletes(word) + self.substitutions(word)
			output = newOutput

		return output

	def check_non_words(self, sentence, fallback=False):
		output = []
		for word in sentence:
			if word in self.language_model:
				output.append([word])
			else:
				L = self.generate_candidates(word)
				if fallback && len(L) == 0:
					output.append([word])
				else:
					L.sort(key=lambda w: self.language_model.unigram_score(w) + self.channel_model.align(w)[0])
					output.append(L)
		return output

	def check_sentence(self, sentence, fallback=False):
		return self.check_non_words(sentence, fallback)

	def check_text

	def check_sentence(self, sentence, fallback=False):

