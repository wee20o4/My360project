import requests

def get_data_from_api(url):
    try:
        # Thêm timeout để tránh treo lâu nếu server không phản hồi
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        return None

def analyze_data(posts):
    if not posts:
        print("Không có dữ liệu để phân tích.")
        return

    user_post_count = {}
    for post in posts:
        user_id = post['userId']
        user_post_count[user_id] = user_post_count.get(user_id, 0) + 1

    print("Số lượng bài viết theo userId:")
    for user_id, count in user_post_count.items():
        print(f"User {user_id}: {count} posts")

if __name__ == "__main__":
    api_url = "https://jsonplaceholder.typicode.com/posts"
    data = get_data_from_api(api_url)
    analyze_data(data)
