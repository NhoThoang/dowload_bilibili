import tkinter as tk
from tkinter import filedialog, scrolledtext
import yt_dlp

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("600x400")
        
        tk.Label(root, text="Mỗi link là 1 dòng trong file text", font=("Arial", 12)).pack(pady=5)
        
        self.file_label = tk.Label(root, text="Chưa chọn file", fg="blue")
        self.file_label.pack()
        
        tk.Button(root, text="Chọn file txt", command=self.select_file).pack(pady=5)
        
        self.text_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.text_area.pack()
        
        tk.Label(root, text="Design by: Nguyễn Nho Thoáng", font=("Arial", 10, "bold"), fg="gray").pack(pady=5)
    
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.file_label.config(text=file_path)
            self.process_file(file_path)
    
    def process_file(self, file_path):
        with open(file_path, "r") as file:
            urls = file.readlines()
        
        for url in urls:
            url = url.strip()
            if url:
                status = self.check_downloadable(url)
                self.text_area.insert(tk.END, url + " - " + ("✅ Tải được" if status else "❌ Không tải được") + "\n", "green" if status else "red")
                self.text_area.see(tk.END)
    
    def check_downloadable(self, url):
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
                return bool(info.get("formats"))
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()