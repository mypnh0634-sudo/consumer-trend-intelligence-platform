import sys
import os
import sqlite3
import json
import pandas as pd
from datetime import datetime

# Bổ sung đường dẫn hệ thống để gọi được thư mục config ngang hàng
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import logger
from analyzer.nlp_analyzer import NLPAnalyzer

class ReportExporter:
    """
    Module phụ trách trích xuất dữ liệu tổng hợp từ Database, 
    kết hợp tính toán NLP và xuất ra các định dạng báo cáo vật lý (Excel, JSON).
    """

    def __init__(self, db_path: str = "database/trend_intelligence.db"):
        self.db_path = db_path
        self.analyzer = NLPAnalyzer()

    def _load_data_from_db(self) -> list:
        """Đọc toàn bộ video lưu trong DB ra để chuẩn bị xử lý"""
        if not os.path.exists(self.db_path):
            logger.error("Không tìm thấy file Database để xuất báo cáo.")
            return []
            
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tiktok_videos")
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Lỗi khi đọc dữ liệu từ DB: {e}")
            return []

    def export_all(self, output_dir: str = "output"):
        """Vận hành xuất đồng thời cả file Excel báo cáo và file JSON thô"""
        os.makedirs(output_dir, exist_ok=True)
        raw_videos = self._load_data_from_db()
        
        if not raw_videos:
            logger.warning("Không có dữ liệu trong Database để tiến hành xuất báo cáo.")
            return

        processed_data = []
        logger.info("Đang xử lý làm giàu chỉ số dữ liệu cho báo cáo thị trường...")
        
        for video in raw_videos:
            # Tái tính toán ER và Keywords để nhét vào file báo cáo
            er = self.analyzer.calculate_engagement(video)
            keywords = self.analyzer.extract_keywords(video.get("caption", ""))
            
            video_report = dict(video)
            video_report["engagement_rate_pct"] = er
            video_report["extracted_keywords"] = ", ".join(keywords)
            processed_data.append(video_report)

        # Định dạng tên file theo ngày hiện tại
        current_date = datetime.now().strftime("%Y%m%d")
        excel_path = os.path.join(output_dir, f"market_report_{current_date}.xlsx")
        json_path = os.path.join(output_dir, f"market_data_{current_date}.json")

        try:
            # 1. Xuất báo cáo Excel bằng Pandas
            df = pd.DataFrame(processed_data)
            df.to_excel(excel_path, index=False, engine='openpyxl')
            logger.info(f"Xuất báo cáo Excel thành công: {excel_path}")

            # 2. Xuất dữ liệu JSON cấu trúc sạch
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)
            logger.info(f"Xuất file dữ liệu JSON thành công: {json_path}")

        except Exception as e:
            logger.error(f"Gặp lỗi khi ghi file báo cáo vật lý: {e}")

if __name__ == "__main__":
    exporter = ReportExporter()
    exporter.export_all()