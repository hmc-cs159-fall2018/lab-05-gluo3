from EditDistance import EditDistanceFinder
from LanguageModel import LanguageModel
import spacy
import string


PUNCTUATION = ".?!:;\"'\n,/\\"
class SpellChecker():

	def __init__(self, max_distance, channel_model=None, language_model=None):
		self.nlp = spacy.load("en")
		self.channel_model = channel_model
		self.language_model = language_model
		self.max_distance = max_distance

	def load_channel_model(self, fp):
		self.channel_model = EditDistanceFinder()
		self.channel_model.load(fp)

	def load_language_model(self, fp):
		self.language_model = LanguageModel()
		self.language_model.load(fp)

	def bigram_score(self, prev_word, focus_word, next_word):
		return (self.language_model.bigram_prob(prev_word,focus_word) + self.language_model.bigram_prob(focus_word,next_word))/2

	def unigram_score(self, word):
		return self.language_model.unigram_prob(word)

	def cm_score(self, error_word, corrected_word):
		return self.channel_model.prob(error_word,corrected_word)

	def isSubstring(self, w1, w2):
		if w1 == "":
			return True
		elif w2 == "":
			return False
		else:
			if w1[0] == w2[0]:
				return self.isSubstring(w1[1:], w2[1:])
			else:
				return self.isSubstring(w1, w2[1:])

	def inserts(self, word):
		output = []
		for w in self.language_model.vocabulary:
			if len(w) == len(word) + 1:
				if self.isSubstring(word, w):
					output.append(w)
		return output

	def deletes(self, word):
		output = []
		for w in self.language_model.vocabulary:
			if len(w) == len(word) - 1:
				if self.isSubstring(w,word):
					output.append(w)
		return output

	def substitutions(self, word):
		output = []
		for w in self.language_model.vocabulary:
			if len(w) == len(word):
				numInc = 0
				for i in range(len(w)):
					if w[i] != word[i]:
						numInc += 1
				if numInc == 1:
					output.append(w)
		return output

	def generate_candidates(self, word):
		output = []
		newWords = [word]
		for _ in range(self.max_distance):
			checkWords = []
			for w in newWords:
				if not all([x in string.ascii_lowercase for x in w]):
					continue
				checkWords.extend(self.inserts(word))
				checkWords.extend(self.deletes(word))
				checkWords.extend(self.substitutions(word))
			output.extend(checkWords)
			newWords = checkWords

		return list(set(output))

	def sortList(self, wordList, prevWord, targetWord, nextWord):
		output = []
		for word in wordList:
			bs = self.bigram_score(prevWord, word, nextWord)
			us = self.unigram_score(word)
			cm = self.cm_score(targetWord, word)
			score = 0.5*cm + 0.25*bs + 0.25*us
			output.append((word,score))
		output.sort(key=lambda w: w[1])
		return [w[0] for w in output]

	def check_non_words(self, sentence, fallback=False):
		output = []
		for i in range(len(sentence)):
			if sentence[i] in self.language_model:
				output.append([sentence[i]])
			else:
				L = self.generate_candidates(sentence[i])
				if fallback and len(L) == 0:
					output.append([sentence[i]])
				else:
					if i > 0:
						prevWord = sentence[i-1]
					else:
						prevWord = "<s>"
					if i+1 == len(sentence):
						nextWord = "</s>"
					else:
						nextWord = sentence[i+1]
					self.sortList(L, prevWord, sentence[i], nextWord)
					output.append(L)
		return output

	def check_sentence(self, sentence, fallback=False):
		return self.check_non_words(sentence, fallback)

	def check_line(self, line, fallback=False):
		sentences = self.nlp(line).sents
		output = []
		for sent in sentences:
			sentence = [str(w) for w in sent]
			output.extend(self.check_sentence(sentence, fallback=fallback))

		return output

	def check_text(self, text, fallback=False):
		sentences = self.nlp(text).sents
		output = []
		for sent in sentences:
			output.append(self.check_sentence(sent,fallback))
		return output

	def autocorrect_sentence(self, sentence):
		suggestions = self.check_sentence(sentence, True)
		return [word[0] for word in suggestions]

	def autocorrect_line(self, line):
		sentences = self.nlp(line).sents
		output = []

		for sent in sentences:
			sentence = [str(w) for w in sent]
			output.extend(self.autocorrect_sentence(sentence))

		return output

	def suggest_sentence(self, sentence, max_suggestions):
		suggestions = self.check_sentence(sentence, True)
		output = []

		for i in range(len(sentence)):
			if sentence[i] in self.language_model:
				output.append(sentence[i])
			else:
				output.append(suggestions[i][0:max_suggestions])

		return output

	def suggest_line(self, line, max_suggestions):
		sentences = self.nlp(line).sents
		output = []

		for sent in sentences:
			sentence = [str(w) for w in sent]
			output.extend(self.suggest_sentence(sentence,max_suggestions))

		return output

	def suggest_text(self, text, max_suggestions):
		sentences = self.nlp(text).sents
		output = []

		for sent in sentences:
			suggestion = self.suggest_sentence(sent, max_suggestions)
			for sug in suggestion:
				output.append(sug)

		return output