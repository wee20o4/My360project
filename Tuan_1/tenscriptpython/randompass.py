import random
import string

def tao_mk(dai):
    if dai < 4:
        return None

    thuong = random.choice(string.ascii_lowercase)
    hoa = random.choice(string.ascii_uppercase)
    so = random.choice(string.digits)
    dac_biet = random.choice("!@#$%^&*()-_=+[]{}|;:,.<>?")

    tat_ca = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    con_lai = [random.choice(tat_ca) for _ in range(dai - 4)]

    mk_list = list(thuong + hoa + so + dac_biet + ''.join(con_lai))
    random.shuffle(mk_list)
    return ''.join(mk_list)

while True:
    try:
        n = int(input("Nhập số ký tự cho mật khẩu (≥ 4): "))
        mk = tao_mk(n)
        if mk:
            print("Mật khẩu được tạo:", mk)
            break
        else:
            print("Độ dài quá ngắn, phải từ 4 trở lên.")
    except ValueError:
        print("Vui lòng nhập một số nguyên.")
