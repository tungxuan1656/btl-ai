import random
from .score import score


class break_cipher():
    'Công cụ phá mật mã'

    # hàm khởi tạo
    def __init__(self, ngrams, ciphertext):
        # định nghĩa thuộc tính của lớp, thuộc tính là có self.
        self._sc = score(self._openfile(ngrams))
        self._ctext = ciphertext
        self._ptext = ''  # plaintext
        self._bscore = -99e9  # best score tìm được
        self._bkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')  # best key tìm được
        self._bkeyencryp = list()
        self._s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self._ptable = self._s.maketrans(self._s, ''.join(self._bkey))

    # bắt đầu giải mã
    def start_break(self):
        pass

    # show kết quả ra ngoài màn hình
    def _show(self, i):
        print('\n--- Tìm thấy chuỗi tin tốt hơn trong lần ' + str(i))
        print('\t- Điểm số: ' + str(self._bscore))
        print('\t- Khóa giải mã: ' + ''.join(self._bkey))
        print('\t- Khóa mã hóa: ' + ''.join(self._bkeyencryp))
        print('\t> Chuỗi được giải mã: ' + self._ptext)

    # lưu lại kết quả vào file
    def _savefile(self, i):
        fo = open('result.txt', 'a', encoding='utf-8')
        if (i == 1):
            fo.write('\n\n______________________________________________________')
            fo.write('\nCipher text input: ' + self._ctext)
        fo.write('\n\n--- Tìm thấy chuỗi tin tốt hơn trong lần ' + str(i))
        fo.write('\n\t- Điểm số: ' + str(self._bscore))
        fo.write('\n\t- Khóa giải mã: ' + ''.join(self._bkey))
        fo.write('\n\t- Khóa mã hóa: ' + ''.join(self._bkeyencryp))
        fo.write('\n\t> Chuỗi được giải mã: ' + self._ptext)
        fo.close()

    # tính điểm dựa vào key cục bộ truyền vào
    def _scoring(self, listkey):
        # tạo 1 bảng thay thế
        self._ptable = self._s.maketrans(self._s, ''.join(listkey))
        # thay thế tìm ra plaintext
        self._ptext = self._ctext.translate(self._ptable)
        # tính điểm plaintext tìm được
        pscore = self._sc.scoring(self._ptext)

        return pscore

    # mở file data tùy theo lựa chọn của người dùng
    def _openfile(self, ngrams):
        # biến file là biến cục bộ của hàm không phải thuộc tính
        if (ngrams == 2):
            # đường dẫn tương đối tính từ file chứa hàm main
            file = open('data/bigrams.txt', 'r')
        elif (ngrams == 3):
            file = open('data/trigrams.txt', 'r')
        else:
            file = open('data/quadgrams.txt', 'r')

        return file

    # tìm ra key mã hóa dựa trên bảng phá mã
    def _keyencryp(self, ptable):
        l = list()
        for i in sorted(ptable.items(), key=lambda x: x[1]):
            l.append(chr(i[0]))
        return l
