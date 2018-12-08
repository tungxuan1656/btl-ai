#!/usr/bin/python
# -*- coding: utf8 -*-

import random
import os
import re
import sys
from transform.break_cipher import break_cipher


# ngăn không cho hiển thị traceback (mã lỗi ngoại lệ)
sys.tracebacklimit = 0

print('Lựa chọn kiểu nhập chuỗi:')
print('\tNhập chuỗi cần giải mã từ file, nhập vào 1.')
print('\tNhập chuỗi cần giải mã từ bàn phím, nhập vào 2.')
ip = int(input('\tLựa chọn: '))
if(ip == 1):
    s = input('\nNhập tên file chứa chuỗi trong cùng thư mục: ')
    file_input = open(s, 'r')
    s = file_input.read()
    file_input.close()
elif(ip == 2):
    s = input('\nNhập chuỗi cần giải mã: ')
else:
    input('\n---> Lựa chọn không đúng, thoát chương trình!')
    os._exit(1)

print('\nLựa chọn sử dụng bộ dữ liệu để giải mã:')
print('\tChọn bộ 2 (bigrams) nhập 2.')
print('\tChọn bộ 3 (trigrams) nhập 3.')
print('\tChọn bộ 4 (quadgrams) nhập 4.')
n = int(input('\tNhập lựa chọn: '))
while(n not in (2, 3, 4)):
    n = int(input('\tNhập không đúng, mời nhập lại: '))

# loại bỏ ký tự ngoài chữ cái trong ciphertext
s = re.sub('[^A-Z]', '', s.upper())
print('\nKhi giải mã nhấn "Ctrl + c" để dừng!\nBắt đầu giải mã:')
break_ = break_cipher(n, s)
break_.start_break()
