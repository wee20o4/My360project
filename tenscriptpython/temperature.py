temp = float(input("Nhập nhiệt độ: "))
unit = input("Nhập đơn vị (C cho độ C hoặc F cho độ F): ").upper()

if unit == "C":
    result = (temp * 9/5) + 32
    print(f"{temp} độ C = {result} độ F")

elif unit == "F":
    result = (temp - 32) * 5/9
    print(f"{temp} độ F = {result} độ C")
else:
    print("Đơn vị không hợp lệ! Vui lòng nhập C hoặc F.")

# Nhập nhiệt độ: 15
# Nhập đơn vị (C cho độ C hoặc F cho độ F): C
# 15.0 độ C = 59.0 độ F