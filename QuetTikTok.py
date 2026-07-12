import yt_dlp
import pandas as pd
import os
os.makedirs("output", exist_ok=True)
print("=" * 50)
print("CÔNG CỤ PHÂN TÍCH TIKTOK")
print("=" * 50)

username = input("Nhập username TikTok (không có @): ")

url = f"https://www.tiktok.com/@{username}"

ydl_opts = {
    "quiet": True,
    "extract_flat": True,
    "playlistend": 50
}
print("Đang lấy danh sách video...")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)

import pandas as pd

videos = []

for video in info["entries"]:
    videos.append({
        "ID": video.get("id"),
        "Tiêu đề": video.get("title"),
        "Lượt xem": video.get("view_count"),
        "Lượt thích": video.get("like_count"),
        "Bình luận": video.get("comment_count"),
        "Ngày đăng": video.get("upload_date"),
        "Link": f"https://www.tiktok.com/@{username}/video/{video.get('id')}"
    })

df = pd.DataFrame(videos)

df.to_excel("output/all_videos.xlsx", index=False)

print(f"Đã lưu {len(df)} video.")