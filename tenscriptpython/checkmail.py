import re

email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

with open('dataemail.txt', 'r') as file:
    emails = file.readlines()

for email in emails:
    email = email.strip()
    if email_pattern.match(email):
        print(f"Hợp lệ   : {email}")
    else:
        print(f"Không hợp lệ: {email}")


#Hợp lệ   : valid.email@example.com
#Hợp lệ   : test123@domain.co
#Không hợp lệ: wrong-email@@com
#Không hợp lệ: missingatsymbol.com