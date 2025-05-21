import yt_dlp

def get_best_format(url):
    """Lấy định dạng video & audio tốt nhất từ URL"""
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        best_video = None
        best_audio = None
        # Lọc video và audio tốt nhất
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('acodec') == 'none':  # Chỉ video
                if not best_video or f['height'] > best_video['height']:  # Chọn video độ phân giải cao nhất
                    best_video = f
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':  # Chỉ audio
                if not best_audio or f['abr'] > best_audio['abr']:  # Chọn audio bitrate cao nhất
                    best_audio = f

        if best_video and best_audio:
            print(f"✅ Chọn video: {best_video['format_id']} ({best_video['height']}p)")
            print(f"✅ Chọn audio: {best_audio['format_id']} ({best_audio['abr']}kbps)")
            return f"{best_video['format_id']}+{best_audio['format_id']}"
        else:
            print("❌ Không tìm thấy định dạng phù hợp!")
            return None


def download_video(url):
    """Tải video với định dạng tốt nhất"""
    best_format = get_best_format(url)
    if not best_format:
        print("❌ Không thể tải video.")
        return

    ydl_opts = {
        'format': best_format,
        'outtmpl': '%(title)s.%(ext)s',  # Đặt tên file theo tiêu đề video
        'merge_output_format': 'mp4',  # Xuất ra MP4
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print("✅ Tải video hoàn tất!")


# === Gọi hàm với URL cần tải ===
video_url = "https://www.bilibili.com/video/BV1xx411c7mD"
download_video(video_url)
