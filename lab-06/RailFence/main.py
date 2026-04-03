import sys
from PyQt5 import QtWidgets, uic

# --- THUẬT TOÁN RAIL FENCE (MÃ HÓA) ---
def encrypt_rail_fence(text, key):
    if key == 1: return text
    rail = [['\n' for i in range(len(text))] for j in range(key)]
    dir_down = False
    row, col = 0, 0
    for char in text:
        if row == 0 or row == key - 1: dir_down = not dir_down
        rail[row][col] = char
        col += 1
        row += 1 if dir_down else -1
    return "".join([rail[i][j] for i in range(key) for j in range(len(text)) if rail[i][j] != '\n'])

# --- THUẬT TOÁN RAIL FENCE (GIẢI MÃ) ---
def decrypt_rail_fence(cipher, key):
    if key == 1: return cipher
    rail = [['\n' for i in range(len(cipher))] for j in range(key)]
    dir_down = None
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0: dir_down = True
        if row == key - 1: dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0: dir_down = True
        if row == key - 1: dir_down = False
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1
    return "".join(result)

# --- LỚP ĐIỀU KHIỂN GIAO DIỆN ---
class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        # Chú ý: Đường dẫn này phải khớp với vị trí file .ui của bạn
        try:
            uic.loadUi('lab-06/RailFence/railfence.ui', self)
        except:
            uic.loadUi('railfence.ui', self) # Sơ cua nếu bạn đã cd vào thư mục RailFence
        
        # Kết nối nút bấm (Đúng Object Name Bảo Anh đã đặt)
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)

    def handle_encrypt(self):
        # Lấy text từ QPlainTextEdit dùng .toPlainText()
        text = self.txt_plain.toPlainText()
        try:
            # Lấy key từ ô txt_key (kiểm tra cả QLineEdit và QPlainTextEdit)
            if hasattr(self.txt_key, 'text'):
                key = int(self.txt_key.text())
            else:
                key = int(self.txt_key.toPlainText())
            
            self.txt_cipher.setPlainText(encrypt_rail_fence(text, key))
        except ValueError:
            self.txt_cipher.setPlainText("Lỗi: Key phải là số nguyên!")

    def handle_decrypt(self):
        cipher = self.txt_cipher.toPlainText()
        try:
            if hasattr(self.txt_key, 'text'):
                key = int(self.txt_key.text())
            else:
                key = int(self.txt_key.toPlainText())
                
            self.txt_plain.setPlainText(decrypt_rail_fence(cipher, key))
        except ValueError:
            self.txt_plain.setPlainText("Lỗi: Key phải là số nguyên!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())