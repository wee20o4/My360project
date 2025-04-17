import os

def tinh_tong(file_path):
    if not os.path.exists(file_path):
        print("File không tồn tại.")
        return

    tong = 0
    with open(file_path, 'r') as f:
        for line in f:
            try:
                tong += float(line.strip())
            except ValueError:
                continue

    print(f"Tổng các số trong file là: {tong}")

file_path = "sumdata.txt"
tinh_tong(file_path)

# Tổng các số trong file là: 54.0