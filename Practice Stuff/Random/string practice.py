str = "Barack Obama, Sarah Palin, pool, tears,"

list = []
terms = str.split(",")
for word in terms:
    tmp = word.strip()
    if tmp:
        list.append(tmp)

print(list)

