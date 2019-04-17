from nltk.translate import bleu_score

from model import Sentence
from sentence_compress import SentenceCompress
import parse

def get_test_data(filename):
	with open(filename, 'r') as f:
		original = []
		compressed = []
		for i, line in enumerate(f):
			sentence = line.strip()
			if i % 2 == 0:
				words = parse.word_tokenize_sent(sentence)
				original.append(Sentence(sentence, words))
			else:
				compressed.append(sentence)
	return original, compressed

def test_sentence_compress():
	test_data_filename = '../data/compress_data.txt'
	original, compressed = get_test_data(test_data_filename)
	compressor = SentenceCompress()
	compressor.syntax_parse(original[:30]) # for testing I'm generally making this smaller
	compressed_prediction = compressor.compress()
	scores = []
	for i, s in enumerate(compressed_prediction):
		score = bleu_score.sentence_bleu([compressed[i]], s)
		scores.append(score)
	return compressed, compressed_prediction, scores

if __name__ == '__main__':
	compressed, compressed_prediction, scores = test_sentence_compress()
	for i, s in enumerate(compressed_prediction):
		print(compressed[i])
		print(s)
		print(scores[i], '\n')


# Example:
# Serge Ibaka -- the Oklahoma City Thunder forward who was born in the Congo but played in Spain -- has been granted Spanish citizenship and will play for the country in EuroBasket this summer, the event where spots in the 2012 Olympics will be decided.
# Serge Ibaka has been granted Spanish citizenship and will play in EuroBasket.
# Serge Ibaka has been granted Spanish citizenship and will play for the country in EuroBasket this summer, the event.
# 0.6526530205320725 