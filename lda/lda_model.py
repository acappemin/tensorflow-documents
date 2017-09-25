import random
import numpy as np
import tensorflow as tf


class LDA(object):

	@staticmethod
	def random_choose(n):
		return random.randint(0, n - 1)

	@staticmethod
	def distributed_choose(distribution):
		summation = sum(distribution)
		if summation > 0:
			distribution = [p / summation for p in distribution]
		else:
			distribution = [1.0 / len(distribution) for _ in distribution]
		threashold = random.random()
		summation = 0
		for index, p in enumerate(distribution):
			summation += p
			if summation >= threashold:
				return index
		raise Exception('Invalid Distribution %s' % str(distribution))

	def __init__(self, documents, K, V):
		self.documents = documents
		self.M = len(self.documents)   # documents
		self.K = K   # topics
		self.V = V   # words
		self.N = [len(document) for document in self.documents]
		self.Nm = np.zeros([self.M], dtype=np.int64)
		self.Nk = np.zeros([self.K], dtype=np.int64)
		self.Nkm = np.zeros([self.K, self.M], dtype=np.int64)
		self.Nkv = np.zeros([self.K, self.V], dtype=np.int64)

		self.alpha = np.ones([self.K], dtype=np.float64) * 0.1
		self.beta = np.ones([self.V], dtype=np.float64) * 0.001
		self.sum_alpha = sum(self.alpha)
		self.sum_beta = sum(self.beta)
		self.theta = np.zeros([self.M, self.K], dtype=np.float64)
		self.fi = np.zeros([self.K, self.V], dtype=np.float64)

		self.topics = [[0] * Nm for Nm in self.N]
		for m in xrange(self.M):
			for n in xrange(self.N[m]):
				# randomly assign topic
				v = self.documents[m][n]
				k = self.random_choose(self.K)
				self.topics[m][n] = k
				self.update_statistics(m, k, v, 1, update=False)

		self.update_contributions()
		print 'finish initialization'

	def iterate(self):
		update = 0
		for m in xrange(self.M):
			for n in xrange(self.N[m]):
				# reassign topic
				v = self.documents[m][n]
				k = self.topics[m][n]
				self.update_statistics(m, k, v, -1)
				prob = [self.generation_probability(m, all_k, v) for all_k in xrange(self.K)]
				new_k = self.distributed_choose(prob)
				self.topics[m][n] = new_k
				self.update_statistics(m, new_k, v, 1)

				if new_k != k:
					update += 1
		print 'Update Number %d, Propotion %f' % (update, float(update) / sum(self.N))

	def update_statistics(self, m, k, v, value, update=True):
		self.Nm[m] += value
		self.Nk[k] += value
		self.Nkm[k, m] += value
		self.Nkv[k, v] += value
		update and self.update_contributions((m, k, v))

	def update_contributions(self, mkv=None):
		if mkv is None:
			for m in xrange(self.M):
				for k in xrange(self.K):
					self.theta[m, k] = (self.Nkm[k, m] + self.alpha[k]) / (self.Nm[m] + self.sum_alpha)
			for k in xrange(self.K):
				for v in xrange(self.V):
					self.fi[k, v] = (self.Nkv[k, v] + self.beta[v]) / (self.Nk[k] + self.sum_beta)
		else:
			m, k, v = mkv
			self.theta[m, k] = (self.Nkm[k, m] + self.alpha[k]) / (self.Nm[m] + self.sum_alpha)
			self.fi[k, v] = (self.Nkv[k, v] + self.beta[v]) / (self.Nk[k] + self.sum_beta)

	def generation_probability(self, m, k, v):
		p_k_given_m = self.topic_distribution_of_document(m, k)
		p_v_given_k = self.word_distribution_of_topic(k, v)
		p_vk_given_m = p_k_given_m * p_v_given_k
		return p_vk_given_m

	def topic_distribution_of_document(self, m=None, k=None):
		if m is None:
			return self.theta
		if k is None:
			return self.theta[m, :]
		else:
			return self.theta[m, k]

	def word_distribution_of_topic(self, k=None, v=None):
		if k is None:
			return self.fi
		if v is None:
			return self.fi[k, :]
		else:
			return self.fi[k, v]

