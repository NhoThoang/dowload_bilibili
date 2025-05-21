import tkinter as tk
from tkinter import filedialog, scrolledtext
import yt_dlp
import threading

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
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
            self.text_area.insert(tk.END, f"Đang tải: {url}\n", "blue")
            self.text_area.see(tk.END)
            
            status = self.download_video(url)
            
            if status:
                self.text_area.insert(tk.END, f"{url} - ✅ Tải xong\n", "green")
            else:
                self.text_area.insert(tk.END, f"{url} - ❌ Tải thất bại\n", "red")
            
            self.text_area.see(tk.END)
        self.text_area.insert(tk.END, "Tải xong\n", "blue")
    
    def download_video(self, url):
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                if not formats:
                    return False
                
                best_format = self.get_best_format(formats)
                if not best_format:
                    return False
                
                ydl_opts = {
                    'format': best_format,
                    'outtmpl': '%(title)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }]
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return True
        except:
            return False
    
    def get_best_format(self, formats):
        best_video = None
        best_audio = None
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                if not best_video or f['height'] > best_video['height']:
                    best_video = f
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                if not best_audio or f['abr'] > best_audio['abr']:
                    best_audio = f
        
        if best_video and best_audio:
            return f"{best_video['format_id']}+{best_audio['format_id']}"
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
