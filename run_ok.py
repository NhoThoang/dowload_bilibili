import requests
from bs4 import BeautifulSoup
import json
import os
path__thumbnail_bilibili = './database/thumbnail_bilibili'
path__thumbnail_xiaohongshu = './database/thumbnail_xiaohongshu'
path__video_bilibili = './database/video_bilibili'
path__video_xiaohongshu = './database/video_xiaohongshu'
# create_folder
os.makedirs(path__thumbnail_bilibili, exist_ok=True)
os.makedirs(path__thumbnail_xiaohongshu, exist_ok=True)
os.makedirs(path__video_bilibili, exist_ok=True)
os.makedirs(path__video_xiaohongshu, exist_ok=True)
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'vi,vi-VN;q=0.9,th-TH;q=0.8,th;q=0.7,en-PN;q=0.6,en;q=0.5,fr-FR;q=0.4,fr;q=0.3,en-US;q=0.2',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
}
def get_data(url:str, mode:str) -> dict | None:
    if mode == "xiaohongshu":
        response = requests.get(url)
    else:
        response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # script = soup.find('script', text=lambda x: x and 'window.__INITIAL_STATE__' in x)
    script = soup.find('script', string=lambda x: x and 'window.__INITIAL_STATE__' in x)
    if script:
        json_text = script.string.replace('window.__INITIAL_STATE__=', '').strip().replace('undefined', '"undefined"').replace('null', '"null"').replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());", "")
        json_data = json.loads(json_text)
        return json_data

def xiaohongshu_crawler(url) -> tuple:
    data = get_data(url, "xiaohongshu")
    noteDetailMap = next(iter(data["note"]["noteDetailMap"].values()))
    note = noteDetailMap["note"]
    image = note["imageList"][0]["urlDefault"]
    video = note["video"]["media"]["stream"]["h264"][0]["masterUrl"]
    return image, video

def bilibili_crawler(url) -> tuple:
    data = get_data(url, "bilibili")
    image = data["video"]["viewInfo"]["pic"]
    video = data["video"]["playUrlInfo"][0]["url"]
    return image, video

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext
import threading
class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("600x400")
        
        tk.Label(root, text="Mỗi link là 1 dòng trong file text", font=("Arial", 12)).pack(pady=5)
        self.combobox = ttk.Combobox(root, values=["Bilibili", "Xiaohongshu"], state="readonly")
        self.combobox.set("Chọn nguồn video")
        self.combobox.pack(pady=5)        
        self.file_label = tk.Label(root, text="Chưa chọn file", fg="blue")
        self.file_label.pack()
        tk.Button(root, text="Chọn file txt", command=self.select_file).pack(pady=5)
        self.start_button = tk.Button(root, text="Start Download", command=lambda: threading.Thread(target=self.start_download).start(), state=tk.DISABLED)
        self.start_button.pack(pady=5)
        
        self.text_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.text_area.pack()
        
        tk.Label(root, text="Design by: Nguyễn Nho Thoáng", font=("Arial", 10, "bold"), fg="gray").pack(pady=5)
        
        self.file_path = ""
        self.urls = []

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.file_path:
            self.file_label.config(text=self.file_path)
            with open(self.file_path, "r") as file:
                self.urls = [url.strip() for url in file.readlines() if url.strip()]
            self.start_button.config(state=tk.NORMAL)
    def start_download(self):
        for i, url in enumerate(self.urls):
            self.text_area.insert(tk.END, f"Đang tải: {url}\n", "blue")
            self.text_area.see(tk.END)
            status = self.download_video(url, i)
            if status:
                self.text_area.insert(tk.END, f"{url} - ✅ Tải xong\n")
            else:
                self.text_area.insert(tk.END, f"{url} - ❌ Tải thất bại\n")   
            self.text_area.see(tk.END)
        self.text_area.insert(tk.END, "Tải xong\n", "blue")
    
    def download_file(self, url, filename, headers=None, chunk_size=1024*1024):
        try:
            with requests.get(url, stream=True, headers=headers, timeout=30) as r:
                r.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
            return True
        except Exception as e:
            # print(f"❌ Lỗi khi tải {url}: {e}")
            return False

    def download_video(self, url, index=0):
        # print(index)
        try:
            type_download = self.combobox.get()
            if type_download == "Bilibili":
                # print("Tải từ Bilibili")
                link_image, link_video = bilibili_crawler(url=url)
            else:
                # print("Tải từ Xiaohongshu")
                link_image, link_video = xiaohongshu_crawler(url=url)
            # Tải ảnh thumbnail
            filename = f"{path__thumbnail_bilibili if type_download == 'Bilibili' else path__thumbnail_xiaohongshu}/thumbnail_{index}.jpg"
            self.download_file(link_image, filename, headers=headers)
            # Tải video
            filename = f"{path__video_bilibili if type_download == 'Bilibili' else path__video_xiaohongshu}/video_{index}.mp4"
            self.download_file(link_video, filename, headers=headers)
            return True
        except Exception as e:
            # print(f"❌ Lỗi tổng: {e}")
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()

