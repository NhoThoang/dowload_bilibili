# import os
# import requests
# from bs4 import BeautifulSoup
# import json
# import tkinter as tk
# from tkinter import ttk, filedialog, scrolledtext
# import threading
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # Đường dẫn lưu trữ
# path_thumbnail_bilibili = './database/thumbnail_bilibili'
# path_thumbnail_xiaohongshu = './database/thumbnail_xiaohongshu'
# path_video_bilibili = './database/video_bilibili'
# path_video_xiaohongshu = './database/video_xiaohongshu'

# # Tạo thư mục nếu chưa tồn tại
# os.makedirs(path_thumbnail_bilibili, exist_ok=True)
# os.makedirs(path_thumbnail_xiaohongshu, exist_ok=True)
# os.makedirs(path_video_bilibili, exist_ok=True)
# os.makedirs(path_video_xiaohongshu, exist_ok=True)

# # Header mặc định
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'vi,vi-VN;q=0.9,th-TH;q=0.8,th;q=0.7,en-PN;q=0.6,en;q=0.5,fr-FR;q=0.4,fr;q=0.3,en-US;q=0.2',
#     'cache-control': 'max-age=0',
#     'priority': 'u=0, i',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
# }

# # Tạo session với khả năng retry
# def create_session():
#     session = requests.Session()
#     retry = Retry(
#         total=5,
#         backoff_factor=1,
#         status_forcelist=[500, 502, 503, 504],
#         allowed_methods=["HEAD", "GET", "OPTIONS"]
#     )
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)
#     return session

# session = create_session()

# # Hàm lấy dữ liệu từ URL
# def get_data(url: str, mode: str) -> dict | None:
#     try:
#         if mode == "xiaohongshu":
#             response = session.get(url)
#         else:
#             response = session.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         script = soup.find('script', string=lambda x: x and 'window.__INITIAL_STATE__' in x)
#         if script:
#             json_text = script.string.replace('window.__INITIAL_STATE__=', '').strip()
#             json_text = json_text.rstrip(';')
#             json_data = json.loads(json_text)
#             return json_data
#     except Exception as e:
#         print(f"Lỗi khi lấy dữ liệu từ {url}: {e}")
#         return None

# # Hàm crawler cho Xiaohongshu
# def xiaohongshu_crawler(url) -> tuple:
#     data = get_data(url, "xiaohongshu")
#     if data:
#         noteDetailMap = next(iter(data["note"]["noteDetailMap"].values()))
#         note = noteDetailMap["note"]
#         image = note["imageList"][0]["urlDefault"]
#         video = note["video"]["media"]["stream"]["h264"][0]["masterUrl"]
#         return image, video
#     return None, None

# # Hàm crawler cho Bilibili
# def bilibili_crawler(url) -> tuple:
#     data = get_data(url, "bilibili")
#     if data:
#         image = data["video"]["viewInfo"]["pic"]
#         video = data["video"]["playUrlInfo"][0]["url"]
#         return image, video
#     return None, None

# # Hàm tải tệp với xử lý lỗi và retry
# def download_file(url, filename, headers=None, chunk_size=1024*1024):
#     try:
#         with session.get(url, stream=True, headers=headers, timeout=30) as r:
#             r.raise_for_status()
#             with open(filename, "wb") as f:
#                 for chunk in r.iter_content(chunk_size=chunk_size):
#                     if chunk:
#                         f.write(chunk)
#         return True
#     except Exception as e:
#         print(f"Lỗi khi tải {url}: {e}")
#         return False

# # Giao diện người dùng
# class VideoDownloaderApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Video Downloader")
#         self.root.geometry("600x400")

#         tk.Label(root, text="Mỗi link là 1 dòng trong file text", font=("Arial", 12)).pack(pady=5)

#         self.file_label = tk.Label(root, text="Chưa chọn file", fg="blue")
#         self.file_label.pack()

#         self.combobox = ttk.Combobox(root, values=["Bilibili", "Xiaohongshu"], state="readonly")
#         self.combobox.set("Chọn nguồn video")
#         self.combobox.pack(pady=5)

#         tk.Button(root, text="Chọn file txt", command=self.select_file).pack(pady=5)

#         self.start_button = tk.Button(root, text="Start Download", command=lambda: threading.Thread(target=self.start_download).start(), state=tk.DISABLED)
#         self.start_button.pack(pady=5)

#         self.text_area = scrolledtext.ScrolledText(root, width=70, height=15)
#         self.text_area.pack()

#         tk.Label(root, text="Design by: Nguyễn Nho Thoáng", font=("Arial", 10, "bold"), fg="gray").pack(pady=5)

#         self.file_path = ""
#         self.urls = []

#     def select_file(self):
#         self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
#         if self.file_path:
#             self.file_label.config(text=self.file_path)
#             with open(self.file_path, "r", encoding="utf-8") as file:
#                 self.urls = [url.strip() for url in file.readlines() if url.strip()]
#             self.start_button.config(state=tk.NORMAL)

#     def start_download(self):
#         for i, url in enumerate(self.urls):
#             self.text_area.insert(tk.END, f"Đang tải: {url}\n")
#             self.text_area.see(tk.END)
#             status = self.download_video(url, i)
#             if status:
#                 self.text_area.insert(tk.END, f"{url} - ✅ Tải xong\n")
#             else:
#                 self.text_area.insert(tk.END, f"{url} - ❌ Tải thất bại\n")
#             self.text_area.see(tk.END)
#         self.text_area.insert(tk.END, "Tải xong\n")

#     def download_video(self, url, index=0):
#         try:
#             type_download = self.combobox.get()
#             if type_download == "Bilibili":
#                 print("Tải từ Bilibili")
#                 link_image, link_video = bilibili_crawler(url=url)
#                 thumbnail_path = os.path.join(path_thumbnail_bilibili, f"thumbnail_{index}.jpg")
#                 video_path = os.path.join(path_video_bilibili, f"video_{index}.mp4")
#             else:
#                 print("Tải từ Xiaohongshu")
#                 link_image, link_video = xiaohongshu_crawler(url=url)
#                 thumbnail_path = os.path.join(path_thumbnail_xiaohongshu, f"thumbnail_{index}.jpg")
#                 video_path = os.path.join(path_video_xiaohongshu, f"video_{index}.mp4")

#             if not link_image or not link_video:
#                 print(f"Không thể lấy link từ {url}")
#                 return False

#             # Tải ảnh thumbnail
#             download_file(link_image, thumbnail_path, headers=headers)

#             # Tải video
#             download_file(link_video, video_path, headers=headers)

#             return True

#         except Exception as e:
#             print(f"Lỗi tổng: {e}")
#             return False

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VideoDownloaderApp(root)
#     root.mainloop()
