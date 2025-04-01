import os
import pytesseract

# กำหนดตำแหน่งของ tesseract.exe
base_dir = os.path.dirname(os.path.abspath(__file__))
tesseract_path = os.path.join(base_dir, 'tesseract', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path
import pyautogui
import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from googletrans import Translator
import mss
from PIL import Image
import time

# ตั้งค่า OCR
custom_config = r'--oem 3 --psm 6 -l jpn+tha+eng'
translator = Translator()
ocr_paused = False

# ===== GUI SETUP =====
root = tk.Tk()
root.title("OCR & Translate Overlay GUI")
root.geometry("900x600")

text_output = ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12))
text_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

credit_label = tk.Label(root, text="พัฒนาโดย sittiphong pornudomthap | sittiphong@pnru.ac.th",
                        font=("Tahoma", 10), fg="gray")
credit_label.pack(pady=(0, 5))

# ===== FUNCTIONS =====
def select_zone_and_translate():
    screen_width, screen_height = pyautogui.size()

    overlay = tk.Toplevel()
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-alpha', 0.3)
    overlay.attributes('-topmost', True)
    overlay.config(bg='black')
    overlay.title("เลือกโซน OCR")

    start_x = start_y = end_x = end_y = 0
    rect = None
    canvas = tk.Canvas(overlay, cursor="cross", bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_mouse_drag(event):
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        nonlocal end_x, end_y
        end_x, end_y = event.x, event.y
        x1, y1 = min(start_x, end_x), min(start_y, end_y)
        x2, y2 = max(start_x, end_x), max(start_y, end_y)
        overlay.destroy()
        threading.Thread(target=ocr_loop, args=((x1, y1, x2, y2),), daemon=True).start()

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    overlay.mainloop()

def ocr_loop(zone):
    with mss.mss() as sct:
        while True:
            if not ocr_paused:
                x1, y1, x2, y2 = zone
                width, height = x2 - x1, y2 - y1
                monitor = {"top": y1, "left": x1, "width": width, "height": height}
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray, config=custom_config).strip()

                if text:
                    translated = translator.translate(text, dest='th')
                    text_output.insert(tk.END, f"[OCR]\n{text}\n\n[แปลไทย]\n{translated.text}\n\n")
                    text_output.see(tk.END)
                    show_translated_overlay((x1, y1, width, height), translated.text)
                    time.sleep(1)  # ค้าง 1 วินาทีก่อนลบ overlay แล้ววนใหม่
            time.sleep(1)

def show_translated_overlay(pos, translated_text):
    x, y, w, h = pos
    overlay = tk.Toplevel()
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-alpha', 0.9)
    overlay.geometry(f"{w}x{h}+{x}+{y}")

    label = tk.Label(overlay, text=translated_text, wraplength=w-10,
                     justify='left', font=("Tahoma", 14), bg="white", fg="black")
    label.pack(expand=True, fill=tk.BOTH)

    overlay.after(1000, overlay.destroy)  # แสดง overlay แค่ 1 วินาที

def clear_text():
    text_output.delete("1.0", tk.END)

def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_output.get("1.0", tk.END))

def toggle_pause():
    global ocr_paused
    ocr_paused = not ocr_paused
    pause_btn.config(text="Resume" if ocr_paused else "Pause")

# ===== BUTTONS =====
select_btn = tk.Button(btn_frame, text="Select Zone & Translate", width=22, command=select_zone_and_translate)
select_btn.pack(side=tk.LEFT, padx=5)

pause_btn = tk.Button(btn_frame, text="Pause", width=14, command=toggle_pause)
pause_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(btn_frame, text="Save to .txt", width=14, command=save_text)
save_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(btn_frame, text="🧹 Clear Output", width=14, command=clear_text)
clear_btn.pack(side=tk.LEFT, padx=5)

# ===== MAIN LOOP =====
root.mainloop()
