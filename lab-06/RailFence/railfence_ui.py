import tkinter as tk
from tkinter import messagebox

def rail_fence_encrypt(text, key):
    rail = [['\n' for i in range(len(text))] for j in range(key)]
    direction_down = False
    row, col = 0, 0
    for char in text:
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        rail[row][col] = char
        col += 1
        row += 1 if direction_down else -1
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)

def on_encrypt():
    text = entry_text.get()
    try:
        key = int(entry_key.get())
        encrypted = rail_fence_encrypt(text, key)
        label_result.config(text=f"Kết quả: {encrypted}", fg="blue")
    except ValueError:
        messagebox.showerror("Lỗi", "Key phải là số nguyên!")

# Tạo giao diện
root = tk.Tk()
root.title("Trình Bảo Anh - Rail Fence UI")
root.geometry("400x250")

tk.Label(root, text="Nhập văn bản:").pack(pady=5)
entry_text = tk.Entry(root, width=40)
entry_text.pack()

tk.Label(root, text="Nhập Key (số hàng):").pack(pady=5)
entry_key = tk.Entry(root, width=10)
entry_key.pack()

tk.Button(root, text="Mã hóa Rail Fence", command=on_encrypt, bg="green", fg="white").pack(pady=20)
label_result = tk.Label(root, text="Kết quả: ", font=("Arial", 10, "bold"))
label_result.pack()

root.mainloop()