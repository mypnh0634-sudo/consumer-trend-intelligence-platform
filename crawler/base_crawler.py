from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCrawler(ABC):
    """
    Lớp cơ sở trừu tượng (Interface) bắt buộc mọi Module Crawler (TikTok, YouTube, Shopee...) 
    sau này đều phải tuân thủ đúng các hàm chuẩn hóa này.
    """

    @abstractmethod
    def fetch_by_username(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Thu thập danh sách video dựa vào tên tài khoản người dùng"""
        pass

    @abstractmethod
    def fetch_by_keyword(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Thu thập danh sách video dựa vào từ khóa tìm kiếm"""
        pass

    @abstractmethod
    def fetch_by_hashtag(self, hashtag: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Thu thập danh sách video dựa vào hashtag bắt đầu bằng #"""
        pass