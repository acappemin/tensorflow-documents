# -*- encoding:utf-8 -*-

import re
import os
import collections


tar_filename = '20news-18828.tar.gz'
directory = '20news-18828'

# import tarfile
# tar = tarfile.open(tar_filename, 'r')
# tar.extractall()


vocabulary_size = 20000
# vocabulary_size = 52

_WORD_SPILT = re.compile(r"[.,!?\"':;)(]")
_DIGIT_RE = re.compile(r"\d+")


def dirlist(path):
	if not os.path.isdir(path):
		return [path]
	allfiles = []
	filelist = os.listdir(path)
	for filename in filelist:
		filepath = os.path.join(path, filename)
		if os.path.isdir(filepath):
			allfiles.extend(dirlist(filepath))
		else:
			allfiles.append(filepath)
	return allfiles


def sentence2words(sentence):
	words = list()
	for space_separated_fragment in sentence.strip().split():
		words_candidate = re.split(_WORD_SPILT, space_separated_fragment)
		words.extend([re.sub(_DIGIT_RE, '0', w.lower()) for w in words_candidate if w and w.isalnum()])
	return words


def build_vocabulary(documents):
	words = list()
	for m in xrange(len(documents)):
		new_sentence = sentence2words(documents[m])
		words.extend(new_sentence)
		documents[m] = new_sentence

	all_count = collections.Counter(words)
	print 'number of all vocabulary: %d' % len(all_count)
	assert len(all_count) >= vocabulary_size
	count = [['__UNK_', 0]]
	count.extend(all_count.most_common(vocabulary_size - 1))

	dictionary = dict()
	for word, _ in count:
		dictionary[word] = len(dictionary)

	digit_documents = [[] for _ in xrange(len(documents))]
	unk_count = 0
	for m in xrange(len(documents)):
		for word in documents[m]:
			index = dictionary.get(word, 0)
			digit_documents[m].append(index)
			if index == 0:
				unk_count += 1
	count[0][1] = unk_count

	reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))

	return dictionary, reversed_dictionary, documents, digit_documents


def read_files():
	allfiles = dirlist(directory)
	print 'number of documents M: %d' % len(allfiles)
	documents = []
	for file in allfiles:
		with open(file, 'rb') as f:
			lines = f.readlines()
			document = ''.join(lines).replace('\n', ' ')
			documents.append(document)
	dictionary, reversed_dictionary, documents, digit_documents = build_vocabulary(documents)

	return dictionary, reversed_dictionary, documents, digit_documents


def read_toy_documents():
	documents = [
		'today the weather is sunny or rainy wind is huge temperature is very low',
		'i like cute animals like cat dog even rat my favourite is tortoise because easy to raise',
		'i have been to some big cities Beijing Shanghai London but i prefer small beautiful ones like my hometown',
		'pop music has won many fans still classical music is fundamental to art of music',
	]
	dictionary, reversed_dictionary, documents, digit_documents = build_vocabulary(documents)
	return dictionary, reversed_dictionary, documents, digit_documents


dictionary, reversed_dictionary, documents, digit_documents = read_files()
# dictionary, reversed_dictionary, documents, digit_documents = read_toy_documents()
print 'first 10 words: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (
	reversed_dictionary[0], reversed_dictionary[1], reversed_dictionary[2], reversed_dictionary[3],
	reversed_dictionary[4], reversed_dictionary[5], reversed_dictionary[6], reversed_dictionary[7],
	reversed_dictionary[8], reversed_dictionary[9])

