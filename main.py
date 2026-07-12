import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.logger import logger
from crawler.tiktok_crawler import TikTokCrawler
from database.db_manager import DatabaseManager
from analyzer.nlp_analyzer import NLPAnalyzer
from exporter.report_exporter import ReportExporter

def run_pipeline(target: str, mode: str = "username", limit: int = 5):
    """
    Hệ thống Pipeline hoàn chỉnh: 
    Extract -> Transform -> Analyze -> Load -> Export
    """
    logger.info(f"=== KHỞI CHẠY HỆ THỐNG PHÂN TÍCH XU HƯỚNG THỊ TRƯỜNG TOÀN DIỆN ===")
    
    crawler = TikTokCrawler()
    db = DatabaseManager()
    analyzer = NLPAnalyzer()
    exporter = ReportExporter()
    
    raw_data = []
    if mode == "username":
        raw_data = crawler.fetch_by_username(username=target, limit=limit)
    elif mode == "keyword":
        raw_data = crawler.fetch_by_keyword(keyword=target, limit=limit)
    elif mode == "hashtag":
        raw_data = crawler.fetch_by_hashtag(hashtag=target, limit=limit)
        
    if raw_data:
        logger.info("=== GIAI ĐOẠN 2: PHÂN TÍCH VÀ ĐÁNH GIÁ CHỈ SỐ ===")
        for video in raw_data:
            er = analyzer.calculate_engagement(video)
            keywords = analyzer.extract_keywords(video.get("caption", ""))
            logger.info(f"Video ID {video.get('video_id')}: ER = {er}% | Keywords: {len(keywords)}")
            
        logger.info(f"=== GIAI ĐOẠN 3: NẠP VÀO DATABASE CỤC BỘ ===")
        saved_count = db.save_videos(raw_data)
        
        logger.info(f"=== GIAI ĐOẠN 4: XUẤT BÁO CÁO THỊ TRƯỜNG VẬT LÝ ===")
        exporter.export_all()
        
        logger.info(f"=== TOÀN BỘ QUY TRÌNH KẾT THÚC THÀNH CÔNG RỰC RỠ ===")
    else:
        logger.warning("Không trích xuất được dữ liệu đầu vào phù hợp.")

if __name__ == "__main__":
    # Test chạy thực tế lưu dữ liệu sạch và xuất file tự động
    run_pipeline(target="whoisceciii07", mode="username", limit=3)