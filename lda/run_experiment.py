import time
import build_vocabulary
import lda_model
import numpy as np


dictionary, reversed_dictionary, documents, digit_documents = \
	build_vocabulary.dictionary, build_vocabulary.reversed_dictionary,\
	build_vocabulary.documents, build_vocabulary.digit_documents

K = 10
V = build_vocabulary.vocabulary_size

model = lda_model.LDA(digit_documents, K=K, V=V)

epochs = 200
check_epochs = 20
for epoch in xrange(epochs):
	time1 = time.time()
	model.iterate()

	if (epoch + 1) % check_epochs == 0:
		for k in xrange(K):
			fi = model.word_distribution_of_topic()
			# normalize by word
			for v in xrange(V):
				fi[:, v] = fi[:, v]
			words = list()
			for _ in xrange(10):
				fi_k = fi[k, :]
				maximum = max(fi_k)
				index = np.where(fi_k == fi_k.max())[0][0]
				fi_k[index] = 0
				words.append(reversed_dictionary[index])
			print 'Top Words of Topic %d: %s' % (k, str(words))

		for m in xrange(model.M):
			print model.topic_distribution_of_document(m)

	time2 = time.time()
	print 'Time Used of Epoch %d: %fmin' % (epoch, (time2 - time1) / 60)

