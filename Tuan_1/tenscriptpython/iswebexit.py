import requests

danh_sach_trang = [
    "https://www.google.com",
    "https://www.thispagedoesnotexist123.com",
    "https://www.wikipedia.org",
    "https://expired.badssl.com"
]

# Mở (hoặc tạo) file result.txt để ghi kết quả
tep_ket_qua = open("result.txt", "w", encoding="utf-8")

# Lặp qua từng đường dẫn trong danh sách
for trang in danh_sach_trang:
    try:
        tra_ve = requests.get(trang, timeout=5)
        if tra_ve.status_code == 200:
            tep_ket_qua.write(trang + " => Còn tồn tại (200)\n")
        else:
            tep_ket_qua.write(trang + f" => Web die ({tra_ve.status_code})\n")
    except requests.RequestException as loi:
        tep_ket_qua.write(trang + f" => Không truy cập được (Lỗi: {loi.__class__.__name__})\n")

tep_ket_qua.close()

print("Kết quả được luuư trong file 'result.txt'")
