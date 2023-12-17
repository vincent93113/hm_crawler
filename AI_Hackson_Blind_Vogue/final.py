import tkinter as tk
from module.openai.openAI_text2voice import generate_and_play_speech
from module.voice_to_text.voice_to_text import voice_to_text
import pygame as pg
import threading
from module.ImageGeneration.image import ImageGanerate
from io import BytesIO
import requests
from PIL import Image, ImageTk

def show_image_from_url(image_url):
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    # Resize the image 
    (x, y) = img.size
    x_s = 300
    y_s = int(y * x_s / x)
    img = img.resize((x_s, y_s), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img)
    label.image = tk_img

#更新
def update_label():
    recorded_text = voice_to_text()
    label.config(text=recorded_text)
    button.config(text='正在為您查詢...')
    audio_thread = threading.Thread(target=generate_and_play_speech, args=("正在為您查詢"+recorded_text,)) #label跟聲音同時執行
    audio_thread.start()
 
    label.update_idletasks()
    button.pack_forget()
    url, des = ImageGanerate(recorded_text)
    show_image_from_url(url)
    audio_thread = threading.Thread(target=generate_and_play_speech, args=(des,)) #label跟聲音同時執行
    audio_thread.start()


#錄製按鈕(按鈕文字)       
def record_button(text:str):
    global button
    button = tk.Button(root, text=text, command=update_label)
    button.pack(fill="both", expand="y")
    


#step1 -> 建立螢幕
pg.mixer.init()
root = tk.Tk()
root.title("visual.studio")
root.geometry('300x580')

#step2 開啟 > 輸入語音
label = tk.Label(root, text="請說出您想要的衣服款式", font=30, bg='white', pady=20, padx=100, relief="groove")
label.pack(ipadx=100)
audio_thread = threading.Thread(target=generate_and_play_speech, args=("請說出您想要的衣服款式",)) #label跟聲音同時執行
audio_thread.start()
record_button("點擊錄製")

root.mainloop()
