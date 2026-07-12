import sys
import os
from typing import List, Dict, Any

# Bổ sung đường dẫn hệ thống để gọi được thư mục config ngang hàng
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import logger
from crawler.base_crawler import BaseCrawler

class TikTokCrawler(BaseCrawler):
    """
    Module thu thập dữ liệu TikTok kế thừa từ khung BaseCrawler chuẩn dự án.
    Tận dụng công cụ khai thác dữ liệu để chuyển đổi về dữ liệu cấu trúc sạch.
    """
    
    def __init__(self):
        logger.info("Khởi tạo TikTok Crawler thành công.")

    def _clean_data(self, raw_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Hàm nội bộ giúp chuẩn hóa dữ liệu thô thu về theo đúng Mục 4 của Master Prompt"""
        return {
            "video_id": raw_entry.get("id", ""),
            "video_url": raw_entry.get("webpage_url", ""),
            "username": raw_entry.get("uploader_id", raw_entry.get("uploader", "")),
            "creator_name": raw_entry.get("uploader", ""),
            "caption": raw_entry.get("title", ""),
            "duration": raw_entry.get("duration", 0),
            "publish_date": raw_entry.get("upload_date", ""),
            "view_count": raw_entry.get("view_count", 0),
            "like_count": raw_entry.get("like_count", 0),
            "comment_count": raw_entry.get("comment_count", 0),
            "share_count": raw_entry.get("repost_count", 0),
            "hashtags": raw_entry.get("tags", [])
        }

    def fetch_by_username(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        logger.info(f"Bắt đầu cào dữ liệu TikTok cho username: {username} (Giới hạn: {limit} bài)")
        # LƯU Ý KỸ THUẬT: Vòng sau Tech Lead sẽ cấp code tích hợp chi tiết thư viện cào tại đây
        logger.warning("Hàm fetch_by_username đang ở trạng thái chờ tích hợp lõi cào.")
        return []

    def fetch_by_keyword(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        logger.info(f"Bắt đầu cào dữ liệu TikTok theo từ khóa: '{keyword}' (Giới hạn: {limit} bài)")
        logger.warning("Hàm fetch_by_keyword đang ở trạng thái chờ tích hợp lõi cào.")
        return []

    def fetch_by_hashtag(self, hashtag: str, limit: int = 20) -> List[Dict[str, Any]]:
        clean_tag = hashtag.replace("#", "")
        logger.info(f"Bắt đầu cào dữ liệu TikTok theo hashtag: #{clean_tag} (Giới hạn: {limit} bài)")
        logger.warning("Hàm fetch_by_hashtag đang ở trạng thái chờ tích hợp lõi cào.")
        return []

if __name__ == "__main__":
    # Test nhanh cấu trúc chạy nội bộ file xem logger hoạt động tốt không
    crawler = TikTokCrawler()
    crawler.fetch_by_username("whoisceciii07", limit=5)