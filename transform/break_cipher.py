import random
from .score import score


class break_cipher():
    'Công cụ phá mật mã'

    # hàm khởi tạo
    def __init__(self, ngrams, ciphertext):
        # định nghĩa thuộc tính của lớp, thuộc tính là có self.
        self.__sc = score(self.__openfile(ngrams))
        self.__ctext = ciphertext
        self.__ptext = ''  # plaintext
        self.__bscore = -99e9  # best score tìm được
        self.__bkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')  # best key tìm được
        self.__bkeyencryp = list()
        self.__s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.__ptable = self.__s.maketrans(self.__s, ''.join(self.__bkey))

    # bắt đầu phá mã
    def start_break(self):
        pscore, pkey = self.__bscore, self.__bkey[:]
        i = 0

        while 1:
            i += 1
            random.shuffle(pkey)  # tạo key ban đầu bằng cách trộn ngẫu nhiên
            pscore = self.__scoring(pkey)

            # bắt đầu tìm kiếm cục bộ
            # sau khi count = 1000 tức là coi như đã tìm ra được kết quả tốt nhất
            # trong lần tìm kiếm cục bộ đó
            count = 0
            while (count < 1000):
                a = random.randint(0, 25)
                b = random.randint(0, 25)
                child = pkey[:]
                child[a], child[b] = child[b], child[a]

                score_local = self.__scoring(child)
                if (score_local > pscore):
                    pscore = score_local
                    pkey = child[:]
                    ptable = self.__ptable
                    count = 0
                count += 1

            # nếu lần cục bộ này tìm ra kết quả tốt hơn thì ghi nhận nó
            if (pscore > self.__bscore):
                self.__bkey = pkey[:]
                self.__bscore = pscore
                self.__bkeyencryp = self.__keyencryp(ptable)
                self.__show(i)
                self.__savefile(i)

    # show kết quả ra ngoài màn hình
    def __show(self, i):
        print('\n--- Tìm thấy chuỗi tin tốt hơn trong lần ' + str(i))
        print('\t- Điểm số: ' + str(self.__bscore))
        print('\t- Khóa giải mã: ' + ''.join(self.__bkey))
        print('\t- Khóa mã hóa: ' + ''.join(self.__bkeyencryp))
        print('\t> Chuỗi được giải mã: ' + self.__ptext)

    # lưu lại kết quả vào file
    def __savefile(self, i):
        fo = open('result.txt', 'a', encoding='utf-8')
        if (i == 1):
            fo.write('\n\n______________________________________________________')
            fo.write('\nCipher text input: ' + self.__ctext)
        fo.write('\n\n--- Tìm thấy chuỗi tin tốt hơn trong lần ' + str(i))
        fo.write('\n\t- Điểm số: ' + str(self.__bscore))
        fo.write('\n\t- Khóa giải mã: ' + ''.join(self.__bkey))
        fo.write('\n\t- Khóa mã hóa: ' + ''.join(self.__bkeyencryp))
        fo.write('\n\t> Chuỗi được giải mã: ' + self.__ptext)
        fo.close()

    # tính điểm dựa vào key cục bộ truyền vào
    def __scoring(self, listkey):
        # tạo 1 bảng thay thế
        self.__ptable = self.__s.maketrans(self.__s, ''.join(listkey))
        # thay thế tìm ra plaintext
        self.__ptext = self.__ctext.translate(self.__ptable)
        # tính điểm plaintext tìm được
        pscore = self.__sc.scoring(self.__ptext)

        return pscore

    # mở file data tùy theo lựa chọn của người dùng
    def __openfile(self, ngrams):
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
    def __keyencryp(self, ptable):
        l = list()
        for i in sorted(ptable.items(), key=lambda x: x[1]):
            l.append(chr(i[0]))
        return l
