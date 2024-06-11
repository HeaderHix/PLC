import serial
import tkinter as tk
from tkinter import messagebox
import threading

# 시리얼 포트 설정
serial_port = 'COM5'
baud_rate = 115200
ser = None

def init_serial():
    global ser
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Serial port {serial_port} opened successfully")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def send_data(data):
    try:
        if ser and ser.is_open:
            # 16진수 문자열을 바이트 배열로 변환
            hex_data = data
            byte_data = bytes.fromhex(hex_data)

            # 바이트 데이터를 시리얼 포트로 쓰기
            ser.write(byte_data)
            
            print("Data Sent")
        else:
            raise Exception("Serial port not open")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def read_data():
    try:
        while True:
            if ser and ser.is_open:
                if ser.in_waiting > 0:
                    read = ser.read(ser.in_waiting)
                    read_hex = read.hex().upper()
                    text_widget.insert(tk.END, f"Received (HEX): {read_hex}\n")
                    text_widget.see(tk.END)
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("Serial Data Sender")

# 첫 번째 버튼
send_button1 = tk.Button(window, text="Send Data 1", command=lambda: send_data("3A30313033303030313030303842360D0A"))
send_button1.pack(pady=10)

# 두 번째 버튼
send_button2 = tk.Button(window, text="Send Data 2", command=lambda: send_data("3A30111133303030313030303842360D0A"))
send_button2.pack(pady=10)

# 세 번째 버튼 (길이가 더 짧은 데이터)
send_button3 = tk.Button(window, text="Send Data 3", command=lambda: send_data("3A30000000000000000000000000000A"))
send_button3.pack(pady=10)

# 텍스트 위젯 추가
text_widget = tk.Text(window, height=10, width=50)
text_widget.pack(pady=10)

# 시리얼 포트 초기화
init_serial()

# 시리얼 데이터 읽기 스레드 시작
read_thread = threading.Thread(target=read_data, daemon=True)
read_thread.start()

# 윈도우 실행
window.mainloop()

# 윈도우 종료 시 시리얼 포트 닫기
def on_closing():
    if ser and ser.is_open:
        ser.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
