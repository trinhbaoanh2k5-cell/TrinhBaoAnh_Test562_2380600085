import sys
import base64
from PyQt5 import QtWidgets, uic
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# --- LỚP ĐIỀU KHIỂN GIAO DIỆN RSA ---
class RSAApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(RSAApp, self).__init__()
        
        # Tự động tìm file .ui (thử cả 2 đường dẫn phổ biến)
        try:
            uic.loadUi('lab-06/RSA/rsa.ui', self)
        except:
            try:
                uic.loadUi('RSA.ui', self)
            except:
                uic.loadUi('rsa.ui', self)
        
        # Khởi tạo cặp khóa RSA 2048-bit
        self.key = RSA.generate(2048)
        self.pub_key = self.key.publickey()
        
        # Hiển thị trạng thái vào ô Information (dùng đúng objectName)
        self.txt_info.setPlainText("Hệ thống: Đã khởi tạo cặp khóa RSA thành công!")

        # Kết nối nút bấm với hàm xử lý
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)

    def handle_encrypt(self):
        try:
            # Lấy text từ QPlainTextEdit dùng .toPlainText()
            message = self.txt_plain.toPlainText().encode('utf-8')
            
            # Thực hiện mã hóa
            cipher_rsa = PKCS1_v1_5.new(self.pub_key)
            ciphertext = cipher_rsa.encrypt(message)
            
            # Chuyển kết quả sang Base64 để hiển thị dạng chữ
            result_base64 = base64.b64encode(ciphertext).decode('utf-8')
            self.txt_cipher.setPlainText(result_base64)
            self.txt_info.setPlainText("Thông báo: Mã hóa dữ liệu thành công!")
        except Exception as e:
            self.txt_info.setPlainText(f"Lỗi mã hóa: {str(e)}")

    def handle_decrypt(self):
        try:
            # Lấy dữ liệu Base64 từ ô Cipher
            ciphertext_base64 = self.txt_cipher.toPlainText()
            ciphertext = base64.b64decode(ciphertext_base64)
            
            # Thực hiện giải mã
            cipher_rsa = PKCS1_v1_5.new(self.key)
            sentinel = b"Loi giai ma!"
            decrypted = cipher_rsa.decrypt(ciphertext, sentinel)
            
            # Hiển thị lại kết quả gốc
            self.txt_plain.setPlainText(decrypted.decode('utf-8'))
            self.txt_info.setPlainText("Thông báo: Giải mã dữ liệu thành công!")
        except Exception as e:
            self.txt_info.setPlainText(f"Lỗi giải mã: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())