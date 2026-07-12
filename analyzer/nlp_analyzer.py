import sys
import os
import re
from typing import Dict, Any, List

# Bổ sung đường dẫn hệ thống để gọi được thư mục config ngang hàng
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.logger import logger

class NLPAnalyzer:
    """
    Module xử lý ngôn ngữ tự nhiên cơ bản, bóc tách từ khóa/hashtag
    và tính toán các chỉ số tương tác (Engagement) của video.
    """

    def __init__(self):
        logger.info("Khởi tạo Module Phân tích NLP & Chỉ số tương tác thành công.")

    def calculate_engagement(self, video_data: Dict[str, Any]) -> float:
        """
        Tính toán tỷ lệ tương tác (Engagement Rate) dựa trên tổng tương tác chia cho lượt xem.
        Công thức: ER = ((Like + Comment + Share) / Views) * 100
        """
        views = video_data.get("view_count", 0)
        if views == 0:
            return 0.0
        
        likes = video_data.get("like_count", 0)
        comments = video_data.get("comment_count", 0)
        shares = video_data.get("share_count", 0)
        
        # Áp dụng công thức tính tỷ lệ phần trăm tương tác
        er = ((likes + comments + shares) / views) * 100
        return round(er, 2)

    def extract_keywords(self, text: str) -> List[str]:
        """
        Làm sạch văn bản tiêu đề (caption), loại bỏ ký tự đặc biệt,
        tách chữ để trích xuất các từ khóa thô có độ dài từ 3 ký tự trở lên.
        """
        if not text:
            return []
        
        # Chuyển về chữ thường, loại bỏ liên kết và các ký tự đặc biệt
        text_cleaned = re.sub(r'http\s+|www\S+', '', text.lower())
        words = re.findall(r'\b\w[a-văâđêôơưàảãáạằẳẵắặầnẩẫấnậềểễếnệồổỗốnộờởỡớợừửữứự]\b|\b\w{3,}\b', text_cleaned)
        
        # Bỏ các hashtag ra khỏi danh sách từ khóa chính
        keywords = [word for word in words if not word.startswith('_')]
        return list(set(keywords))  # Loại bỏ trùng lặp

if __name__ == "__main__":
    # Test nhanh tính năng phân tích cục bộ
    analyzer = NLPAnalyzer()
    sample_video = {
        "view_count": 10000,
        "like_count": 800,
        "comment_count": 150,
        "share_count": 50
    }
    er_score = analyzer.calculate_engagement(sample_video)
    print(f"\nTỷ lệ tương tác mẫu (Engagement Rate): {er_score}%")