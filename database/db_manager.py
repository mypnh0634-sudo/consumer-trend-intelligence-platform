import sqlite3
import os
import sys
from typing import List, Dict, Any

# Bổ sung đường dẫn hệ thống để gọi được thư mục config ngang hàng
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import logger

class DatabaseManager:
    """
    Quản lý kết nối, khởi tạo cấu trúc bảng và thực hiện các thao tác
    ghi/đọc dữ liệu (ETL Pipeline) vào SQLite cục bộ phục vụ dự án.
    """
    
    def __init__(self, db_path: str = "database/trend_intelligence.db"):
        self.db_path = db_path
        # Đảm bảo thư mục database tồn tại
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Tạo và trả về kết nối tới file cơ sở dữ liệu SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Giúp lấy dữ liệu ra theo dạng key-value giống dictionary
        return conn

    def init_db(self):
        """Khởi tạo cấu trúc bảng lưu trữ thông tin video theo đúng Mục 4 của Master Prompt"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tiktok_videos (
            video_id TEXT PRIMARY KEY,
            video_url TEXT,
            username TEXT,
            creator_name TEXT,
            caption TEXT,
            duration INTEGER,
            publish_date TEXT,
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER,
            share_count INTEGER,
            hashtags TEXT,
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            with self._get_connection() as conn:
                conn.execute(create_table_query)
                conn.commit()
            logger.info("Khởi tạo cấu trúc Database SQLite cục bộ thành công.")
        except Exception as e:
            logger.error(f"Lỗi nghiêm trọng khi khởi tạo cơ sở dữ liệu: {e}")

    def save_videos(self, videos: List[Dict[str, Any]]) -> int:
        """
        Nạp dữ liệu danh sách video vào DB. 
        Nếu video đã tồn tại (trùng video_id), tự động cập nhật lại các chỉ số tương tác mới nhất.
        """
        if not videos:
            logger.warning("Danh sách video trống, bỏ qua tiến trình nạp dữ liệu vào DB.")
            return 0

        insert_query = """
        INSERT INTO tiktok_videos (
            video_id, video_url, username, creator_name, caption, 
            duration, publish_date, view_count, like_count, 
            comment_count, share_count, hashtags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
            view_count = excluded.view_count,
            like_count = excluded.like_count,
            comment_count = excluded.comment_count,
            share_count = excluded.share_count;
        """
        
        saved_count = 0
        try:
            with self._get_connection() as conn:
                for video in videos:
                    # Chuyển mảng hashtag về dạng chuỗi text cách nhau bằng dấu phẩy để lưu vào DB
                    hashtags_str = ",".join(video.get("hashtags", [])) if isinstance(video.get("hashtags"), list) else ""
                    
                    conn.execute(insert_query, (
                        video.get("video_id"),
                        video.get("video_url"),
                        video.get("username"),
                        video.get("creator_name"),
                        video.get("caption"),
                        video.get("duration"),
                        video.get("publish_date"),
                        video.get("view_count"),
                        video.get("like_count"),
                        video.get("comment_count"),
                        video.get("share_count"),
                        hashtags_str
                    ))
                    saved_count += 1
                conn.commit()
            logger.info(f"Pipeline ETL: Đã nạp thành công {saved_count} bản ghi dữ liệu vào Database.")
        except Exception as e:
            logger.error(f"Thao tác nạp dữ liệu thất bại: {e}")
            
        return saved_count

if __name__ == "__main__":
    # Test khởi chạy nội bộ hệ thống DB
    db = DatabaseManager()