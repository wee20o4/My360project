import string
from collections import Counter

text='Ullamco tempor est dolor magna do ullamco cillum. Non commodo mollit cupidatat excepteur cillum in proident aute officia excepteur tempor. Deserunt adipisicing amet exercitation culpa laborum labore. Labore ex proident aute magna tempor aliquip in voluptate Lorem eiusmod sint. Ipsum Lorem aute pariatur reprehenderit sint irure duis commodo esse fugiat tempor velit ex exercitation. Elit veniam laborum fugiat esse deserunt. Voluptate laborum ea anim Lorem mollit cupidatat labore ipsum anim laboris incididunt consequat ea. Nostrud ad qui nisi ut voluptate fugiat aliquip eiusmod id occaecat aliquip ut anim mollit. Dolor commodo est ipsum incididunt enim. Nulla cillum ut mollit velit reprehenderit quis Lorem. Id ut id ea voluptate cupidatat nulla. Cillum ad eu ad esse deserunt amet consectetur cillum eiusmod ipsum commodo. Culpa ea voluptate reprehenderit minim do nostrud et ut et cillum veniam cillum laboris nulla. Eiusmod proident nostrud deserunt reprehenderit id aute consectetur. Ipsum cupidatat aute ad dolore excepteur consequat et sit nisi ad et. Sint est sunt sit veniam consectetur sunt ullamco.'
text = text.lower()
text = text.translate(str.maketrans('', '', string.punctuation))

words = text.split()
word_counts = Counter(words)

most_common_word, frequency = word_counts.most_common(1)[0]

print(f"Từ phổ biến nhất: '{most_common_word}' xuất hiện {frequency} lần.")

#Từ phổ biến nhất: 'cillum' xuất hiện 7 lần.