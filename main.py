import sys
import os

# Bổ sung đường dẫn để hệ thống nhận diện chính xác các gói module nội bộ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.logger import logger
from crawler.tiktok_crawler import TikTokCrawler
from database.db_manager import DatabaseManager

def run_pipeline(target: str, mode: str = "username", limit: int = 5):
    """
    Hàm điều phối toàn bộ vòng đời của dữ liệu:
    Khai thác (Extract) -> Làm sạch (Transform) -> Nạp vào Cơ sở dữ liệu (Load).
    """
    logger.info(f"=== KHỞI CHẠY TIẾN TRÌNH ETL PLATFORM (Chế độ: {mode.upper()}) ===")
    
    # 1. Khởi tạo các thành phần cốt lõi
    crawler = TikTokCrawler()
    db = DatabaseManager()
    
    raw_data = []
    
    # 2. Extract - Thu thập dữ liệu theo chế độ đầu vào (Mục 3 của Master Prompt)
    if mode == "username":
        raw_data = crawler.fetch_by_username(username=target, limit=limit)
    elif mode == "keyword":
        raw_data = crawler.fetch_by_keyword(keyword=target, limit=limit)
    elif mode == "hashtag":
        raw_data = crawler.fetch_by_hashtag(hashtag=target, limit=limit)
    else:
        logger.error(f"Chế độ vận hành '{mode}' không được hệ thống hỗ trợ.")
        return

    # 3. Load - Nạp luồng dữ liệu sạch đã xử lý tự động vào Database
    if raw_data:
        logger.info(f"Đang chuyển tiếp {len(raw_data)} dữ liệu video sang pipeline lưu trữ...")
        saved_count = db.save_videos(raw_data)
        logger.info(f"=== TIẾN TRÌNH ETL HOÀN THÀNH XUẤT SẮC. ĐÃ GHI: {saved_count} BẢN GHI ===")
    else:
        logger.warning("Không có dữ liệu hợp lệ nào được trích xuất để nạp vào hệ thống.")

if __name__ == "__main__":
    # CHẠY THỬ NGHIỆM: Thu thập nhanh 3 video của tài khoản thị trường
    # Anh có thể đổi mode="keyword" và target="Coffee" để test tìm kiếm ở các sprint sau.
    run_pipeline(target="whoisceciii07", mode="username", limit=3)