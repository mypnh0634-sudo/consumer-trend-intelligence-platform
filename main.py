import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.logger import logger
from crawler.tiktok_crawler import TikTokCrawler
from database.db_manager import DatabaseManager
from analyzer.nlp_analyzer import NLPAnalyzer

def run_pipeline(target: str, mode: str = "username", limit: int = 5):
    """
    Hàm điều phối toàn bộ vòng đời dữ liệu mở rộng:
    Extract (Thu thập) -> Transform & Analyze (Làm sạch & Phân tích) -> Load (Lưu trữ).
    """
    logger.info(f"=== KHỞI CHẠY TIẾN TRÌNH ETL & NLP PLATFORM ===")
    
    crawler = TikTokCrawler()
    db = DatabaseManager()
    analyzer = NLPAnalyzer()
    
    raw_data = []
    if mode == "username":
        raw_data = crawler.fetch_by_username(username=target, limit=limit)
    elif mode == "keyword":
        raw_data = crawler.fetch_by_keyword(keyword=target, limit=limit)
    elif mode == "hashtag":
        raw_data = crawler.fetch_by_hashtag(hashtag=target, limit=limit)
        
    if raw_data:
        logger.info("=== BẮT ĐẦU GIAI ĐOẠN PHÂN TÍCH NLP CHỈ SỐ ===")
        for video in raw_data:
            # Tính toán chỉ số sức khỏe của bài viết
            er = analyzer.calculate_engagement(video)
            # Trích xuất từ khóa từ caption bài viết
            keywords = analyzer.extract_keywords(video.get("caption", ""))
            
            logger.info(f"Video ID {video.get('video_id')}: ER = {er}% | Số từ khóa trích xuất: {len(keywords)}")
            
        logger.info(f"Đang chuyển tiếp {len(raw_data)} dữ liệu sang pipeline lưu trữ...")
        saved_count = db.save_videos(raw_data)
        logger.info(f"=== TIẾN TRÌNH HOÀN THÀNH XUẤT SẮC. ĐÃ GHI: {saved_count} BẢN GHI ===")
    else:
        logger.warning("Không có dữ liệu hợp lệ nào được trích xuất.")

if __name__ == "__main__":
    run_pipeline(target="whoisceciii07", mode="username", limit=3)