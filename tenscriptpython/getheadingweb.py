import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com'
response = requests.get(url)

if response.status_code == 200:
    # Phân tích nội dung HTML bằng BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tìm tất cả các quote
    quotes = soup.find_all('span', class_='text')

    print("📌 Các trích dẫn mới nhất:")
    for idx, quote in enumerate(quotes, start=1):
        print(f"{idx}. {quote.get_text()}")
else:
    print(f"Lỗi khi kết nối: {response.status_code}")


# 📌 Các trích dẫn mới nhất:
# 1. “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”
# 2. “It is our choices, Harry, that show what we truly are, far more than our abilities.”
# 3. “There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”
# 4. “The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”
# 5. “Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.”
# 6. “Try not to become a man of success. Rather become a man of value.”
# 7. “It is better to be hated for what you are than to be loved for what you are not.”
# 8. “I have not failed. I've just found 10,000 ways that won't work.”
# 9. “A woman is like a tea bag; you never know how strong it is until it's in hot water.”
# 10. “A day without sunshine is like, you know, night.”