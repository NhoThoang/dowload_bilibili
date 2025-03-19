# import yt_dlp

# # Thay link video bằng video bạn muốn tải
# url = "https://www.bilibili.com/video/BV1xx411c7mD"

# ydl_opts = {
#     'format': 'best',  # Chọn chất lượng cao nhất
#     'outtmpl': '%(title)s.%(ext)s'  # Đặt tên file theo tiêu đề video
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([url])
# import yt_dlp

# url = "https://www.bilibili.com/video/BV1xx411c7mD"

# ydl_opts = {
#     'listformats': True  # Hiển thị danh sách các định dạng
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([url])


import yt_dlp

url = "https://www.bilibili.com/video/BV1xx411c7mD"

ydl_opts = {
    'format': '100023+30232',  # Chọn video (100023) + audio (30232)
    'outtmpl': '%(title)s.%(ext)s',  # Đặt tên file theo tiêu đề video
    'merge_output_format': 'mp4'  # Ghép file thành MP4
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

