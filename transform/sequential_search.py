from .break_cipher import break_cipher
from .score import score
import datetime


class sequential_search(break_cipher):
    'Thuật toán tìm kiếm tuần tự'

    # 26! = 403291461126605635584000000 =))))))))))))
    def __init__(self, ngrams, ciphertext):
        super().__init__(ngrams, ciphertext)
        # Nhóm 1: e
        # Nhóm 2: t, a, o, i, n, s, h, r
        # Nhóm 3: d, l
        # Nhóm 4: c, u, m, w, f, g, y, p, b
        # Nhóm 5: v, k, j, x, q, z
        #
        # Sinh ra cấp mới:
        # Hàng ngang 0 thì theo đúng thứ tự
        # Hàng dọc 0  theo đúng thứ tự trên xuống
        # Hàng ngang i sinh phần tử theo thứ tự:
        #
        # Chữ cái ở vị trí vt0 (theo hàng ngang) thì chia nhóm chữ của chữ cái đó ra làm 2 phần
        # 1 phần bên trái và 1 phần bên phải.
        #
        # Đoạn 1 là chữ cái vt0.
        # Đoạn 2 là phần bên PHẢI của vt0 TRONG NHÓM CỦA NÓ theo ĐÚNG thứ tự.
        # Đoạn 3 là phần bên TRÁI của vt0 TRONG NHÓM CỦA NÓ theo thứ tự NGƯỢC LẠI.
        # Đoạn 4 là NHÓM sau nhóm của vt0 theo ĐÚNG thứ tự.
        # Đoạn 5 là NHÓM trước nhóm của vt0 theo thứ tự NGƯỢC LẠI.
        #
        # Bây giờ coi như đã lấy được 1 đoạn ở giữa của chuỗi đúng thứ tự ban
        # đầu. Tiếp theo xếp 1 nhóm phía bên trái theo đúng thứ tự rồi lại đến
        # 1 nhóm bên phải NGƯỢC LẠI rồi lại đến bên trái, cứ thế như vậy.
        #
        self._matrix = list()
        self._fs = self._frequency_statistics()
        self._ttable = dict()
        self._i = 0

    def _create_matrix(self):
        first = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U',
                 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
        # vị trí bắt đầu và kết thúc
        group_info = ((0, 0), (1, 8), (9, 10), (11, 19), (20, 25))
        self._matrix = list()
        self._matrix.append(first[:])
        for i in range(1, 26):
            self._matrix.append(list())
            # tìm ra nhóm của i, đặt số nhóm vào k
            for j in range(5):
                if (i >= group_info[j][0] and i <= group_info[j][1]):
                    k = j
                    break
            # đoạn 1 và 2
            for j in range(i, group_info[k][1] + 1):
                self._matrix[i].append(first[j])
            # đoạn 3
            for j in reversed(range(group_info[k][0], i)):
                self._matrix[i].append(first[j])

            t = [0, 1, 2, 3, 4]
            z = 0
            t.remove(k)
            # đoạn 4 5 ...
            while (len(t) != 0):
                z += 1
                # nhóm bên trái
                if ((k + z) in t):
                    for j in range(group_info[k + z][0], group_info[k + z][1] + 1):
                        self._matrix[i].append(first[j])
                    t.remove(k + z)
                # nhóm bên phải
                if ((k - z) in t):
                    for j in reversed(range(group_info[k - z][0], group_info[k - z][1] + 1)):
                        self._matrix[i].append(first[j])
                    t.remove(k - z)

    def start_break(self):
        self._create_matrix()
        self._key(0, list())

        # đếm tần suất của các chữ cái trong ciphertext
        # trả về list các chữ cái đã được sắp xếp từ cao xuống thấp
    def _frequency_statistics(self):
        fs = dict()
        for i in self._bkey:
            fs[i] = self._ctext.count(i)
        b = []
        for i in sorted(fs.items(), key=lambda x: x[1]):
            b.append(i[0])
        return b

    def _key(self, k, pkey):
        # khi i = 26 tức là đã đủ pkey
        if (k == 26):
            self._i += 1
            # print(self._i)
            self._ttable.clear()
            for j in range(26):
                self._ttable[self._fs[j]] = pkey[j]
            pkey = []
            for j in sorted(self._ttable.items(), key=lambda x: x[0]):
                pkey.append(j[1])
            pscore = self._scoring(pkey)
            if (pscore > self._bscore):
                self._bkey = pkey[:]
                self._bscore = pscore
                self._bkeyencryp = self._keyencryp(self._ptable)
                self._dt = datetime.datetime.now()
                self._show(self._i)
                self._savefile(self._i)
        else:
            for j in self._matrix[k]:
                if (j not in pkey):
                    temp = pkey[:]
                    # print(j)
                    temp.append(j)
                    self._key(k + 1, temp)
