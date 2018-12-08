import re

s = input('Nhập chuỗi cần mã hóa (English): ')
table = s.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'BVGQKMNADZCWSEOYFJXHTLPUIR')
s_encryp = re.sub('[^A-Z]', '', s.upper()).translate(table)

print('\nChuỗi sau khi được mã hóa là:\n' + s_encryp)
print('\nChuỗi đã được lưu vào file "ciphertext.txt!"')

fo = open('ciphertext.txt', 'w')
fo.write(s_encryp)
fo.close()
