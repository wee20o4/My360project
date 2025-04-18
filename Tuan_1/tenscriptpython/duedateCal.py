from datetime import datetime
# pip install python-dateutil
from dateutil.relativedelta import relativedelta

ngay_bat_dau_str = input("Nhập ngày bắt đầu hợp đồng (dd-mm-yyyy): ")

ngay_bat_dau = datetime.strptime(ngay_bat_dau_str, "%d-%m-%Y")

so_thang = int(input("Nhập thời hạn hợp đồng (số tháng): "))

ngay_het_han = ngay_bat_dau + relativedelta(months=so_thang)

print("Ngày hết hạn hợp đồng là:", ngay_het_han.strftime("%d-%m-%Y"))

# Nhập ngày bắt đầu hợp đồng (dd-mm-yyyy): 15-2-2025
# Nhập thời hạn hợp đồng (số tháng): 5
# Ngày hết hạn hợp đồng là: 15-07-2025