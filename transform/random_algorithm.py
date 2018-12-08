from .break_cipher import break_cipher
from .score import score
import random
import datetime


class random_algorithm(break_cipher):
    'Thuật toán tìm kiếm ngẫu nhiên'

    def __init__(self, ngrams, ciphertext):
        super().__init__(ngrams, ciphertext)

    def start_break(self):
        pscore, tempkey = self._bscore, self._bkey[:]

        i = 0

        while(1):
            i += 1
            pkey = tempkey[:]
            random.shuffle(pkey)
            pscore = self._scoring(pkey)

            if (pscore > self._bscore):
                self._bkey = pkey[:]
                self._bscore = pscore
                self._bkeyencryp = self._keyencryp(self._ptable)
                self._dt = datetime.datetime.now()
                self._show(i)
                self._savefile(i)
