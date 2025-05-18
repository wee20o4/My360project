import unicodedata
import re

def remove_diacritics(text):
    """
    Hàm chuẩn hóa chuỗi văn bản, loại bỏ dấu tiếng Việt để hỗ trợ tìm kiếm không dấu.
    Args:
        text (str): Chuỗi văn bản đầu vào cần chuẩn hóa.
    Returns:
        str: Chuỗi văn bản đã được loại bỏ dấu và thay thế các ký tự đặc biệt như 'đ', 'Đ'.
    """
    text = unicodedata.normalize('NFD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'D')
    return text