from .break_cipher import break_cipher
from .score import score
import random
import datetime


class hill_climbing(break_cipher):
    'Thuật toán leo đồi'

    def __init__(self, ngrams, ciphertext):
        super().__init__(ngrams, ciphertext)

    # bắt đầu phá mã
    def start_break(self):
        pscore, pkey = self._bscore, self._bkey[:]
        i = 0

        while 1:
            i += 1
            random.shuffle(pkey)  # tạo key ban đầu bằng cách trộn ngẫu nhiên
            pscore = self._scoring(pkey)

            # bắt đầu tìm kiếm cục bộ
            # sau khi count = 1000 tức là coi như đã tìm ra được kết quả tốt nhất
            # trong lần tìm kiếm cục bộ đó
            count = 0
            while (count < 1000):
                a = random.randint(0, 25)
                b = random.randint(0, 25)
                child = pkey[:]
                child[a], child[b] = child[b], child[a]

                score_local = self._scoring(child)
                if (score_local > pscore):
                    pscore = score_local
                    pkey = child[:]
                    ptable = self._ptable
                    count = 0
                count += 1

            # nếu lần cục bộ này tìm ra kết quả tốt hơn thì ghi nhận nó
            if (pscore > self._bscore):
                self._bkey = pkey[:]
                self._bscore = pscore
                self._bkeyencryp = self._keyencryp(ptable)
                self._dt = datetime.datetime.now()
                self._show(i)
                self._savefile(i)
