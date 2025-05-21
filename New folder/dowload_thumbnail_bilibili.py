import tkinter as tk
from tkinter import filedialog, scrolledtext
import yt_dlp
import threading
import requests
import os

class ThumbnailDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thumbnail Downloader")
        self.root.geometry("600x400")
        
        tk.Label(root, text="Mỗi link là 1 dòng trong file text", font=("Arial", 12)).pack(pady=5)
        
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
        for url in self.urls:
            self.text_area.insert(tk.END, f"Đang tải thumbnail: {url}\n", "blue")
            self.text_area.see(tk.END)
            
            status = self.download_thumbnail(url)
            
            if status:
                self.text_area.insert(tk.END, f"{url} - ✅ Tải xong\n", "green")
            else:
                self.text_area.insert(tk.END, f"{url} - ❌ Tải thất bại\n", "red")
            
            self.text_area.see(tk.END)
        self.text_area.insert(tk.END, "Tải xong\n", "blue")
    
    def download_thumbnail(self, video_url):
        try:
            with yt_dlp.YoutubeDL({}) as ydl:
                info = ydl.extract_info(video_url, download=False)
                title = info.get("title", "unknown").replace("/", "-")
                thumbnail_url = info.get("thumbnail")
                
                if not thumbnail_url:
                    return False
                
                response = requests.get(thumbnail_url)
                if response.status_code == 200:
                    filename = f"{title}.jpg"
                    with open(filename, "wb") as file:
                        file.write(response.content)
                    return True
                else:
                    return False
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = ThumbnailDownloaderApp(root)
    root.mainloop()