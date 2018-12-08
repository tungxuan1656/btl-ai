from math import log10


class score(object):

    def __init__(self, filedata, sep='\t'):
        self.ngrams = {}
        self.file = filedata
        line = self.file.readline()
        while (line is not ''):
            key, count = line.split(sep)
            self.ngrams[key] = int(count)
            line = self.file.readline()
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        # calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)
        self.floor = log10(0.01 / self.N)

    def scoring(self, text):
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.L + 1):
            if text[i:i + self.L] in self.ngrams:
                score += ngrams(text[i:i + self.L])
            else:
                score += self.floor
        return score
