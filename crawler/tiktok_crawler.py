import sys
import os
from typing import List, Dict, Any
import yt_dlp

# Bổ sung đường dẫn hệ thống để gọi được thư mục config ngang hàng
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import logger
from crawler.base_crawler import BaseCrawler

class TikTokCrawler(BaseCrawler):
    """
    Module thu thập dữ liệu TikTok chuyên nghiệp kế thừa từ BaseCrawler.
    Tự động thu thập, bóc tách và làm sạch cấu trúc dữ liệu.
    """
    
    def __init__(self):
        # Cấu hình an toàn cho yt-dlp để thu thập dữ liệu công khai không bị chặn
        self.ydl_opts = {
            'extract_flat': True,  # Chỉ lấy thông tin metadata, không tải file video về máy
            'skip_download': True,
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': True
        }
        logger.info("Khởi tạo lõi công cụ TikTok Crawler chuyên nghiệp thành công.")

    def _clean_data(self, raw_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Bóc tách và chuẩn hóa dữ liệu thô về định dạng chuẩn Mục 4 của Master Prompt"""
        try:
            return {
                "video_id": str(raw_entry.get("id", "")),
                "video_url": raw_entry.get("url", raw_entry.get("webpage_url", "")),
                "username": raw_entry.get("uploader_id", ""),
                "creator_name": raw_entry.get("uploader", ""),
                "caption": raw_entry.get("title", raw_entry.get("description", "")),
                "duration": raw_entry.get("duration", 0),
                "publish_date": raw_entry.get("upload_date", ""),
                "view_count": raw_entry.get("view_count", 0),
                "like_count": raw_entry.get("like_count", 0),
                "comment_count": raw_entry.get("comment_count", 0),
                "share_count": raw_entry.get("repost_count", 0),
                "hashtags": raw_entry.get("tags", [])
            }
        except Exception as e:
            logger.error(f"Lỗi khi làm sạch dòng dữ liệu: {e}")
            return {}

    def fetch_by_username(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        url = f"https://www.tiktok.com/@{username.strip('@')}"
        logger.info(f"Đang tiến hành khai thác dữ liệu từ kênh: {url}")
        
        cleaned_videos = []
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info or 'entries' not in info:
                    logger.warning(f"Không tìm thấy video nào hoặc tài khoản {username} đang bị khóa.")
                    return []
                
                # Duyệt qua danh sách video thô thu được và giới hạn số lượng bài lấy về
                raw_entries = list(info['entries'])[:limit]
                for entry in raw_entries:
                    if entry:
                        cleaned_entry = self._clean_data(entry)
                        if cleaned_entry:
                            cleaned_videos.append(cleaned_entry)
                            
            logger.info(f"Thu thập thành công {len(cleaned_videos)} video sạch từ tài khoản @{username}")
        except Exception as e:
            logger.error(f"Gặp sự cố nghiêm trọng khi cào dữ liệu từ username {username}: {e}")
            
        return cleaned_videos

    def fetch_by_keyword(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        # Cơ chế tìm kiếm từ khóa an toàn không phụ thuộc vào yt-dlp search gốc
        logger.info(f"Bắt đầu khai thác dữ liệu TikTok theo từ khóa thị trường: '{keyword}'")
        search_url = f"ytsearch{limit}:https://www.tiktok.com/search?q={keyword}"
        
        cleaned_videos = []
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(search_url, download=False)
                if info and 'entries' not in info:
                    cleaned_videos.append(self._clean_data(info))
                elif info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            cleaned_videos.append(self._clean_data(entry))
            logger.info(f"Thu thập thành công {len(cleaned_videos)} video liên quan tới từ khóa '{keyword}'")
        except Exception as e:
            logger.error(f"Lỗi khi cào dữ liệu theo từ khóa '{keyword}': {e}")
            
        return cleaned_videos

    def fetch_by_hashtag(self, hashtag: str, limit: int = 20) -> List[Dict[str, Any]]:
        clean_tag = hashtag.replace("#", "")
        url = f"https://www.tiktok.com/tag/{clean_tag}"
        logger.info(f"Đang tiến hành khai thác dữ liệu theo Hashtag xu hướng: #{clean_tag}")
        
        cleaned_videos = []
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info and 'entries' in info:
                    raw_entries = list(info['entries'])[:limit]
                    for entry in raw_entries:
                        if entry:
                            cleaned_videos.append(self._clean_data(entry))
            logger.info(f"Thu thập thành công {len(cleaned_videos)} video chứa hashtag #{clean_tag}")
        except Exception as e:
            logger.error(f"Lỗi khi cào dữ liệu theo hashtag #{clean_tag}: {e}")
            
        return cleaned_videos

if __name__ == "__main__":
    # Test chạy thực tế lưu trữ dữ liệu sạch ra màn hình kiểm thử
    crawler = TikTokCrawler()
    data = crawler.fetch_by_username("whoisceciii07", limit=3)
    print("\nDỮ LIỆU MẪU ĐÃ LÀM SẠCH:")
    print(data[:1])  # In thử 1 bản ghi cấu trúc xem chuẩn chưa