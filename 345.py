
f_path=r'lianjie.txt'
titlelist =[]
urllist =[]
with open(f_path, encoding='utf-8') as f:
    for line in f:
        title = line.split('-')[0]
        url = line.split('-')[1]
        titlelist.append(title)
        urllist.append(url)
    f.close()
titlelist1=list(set(titlelist))

d1 = {}

value = 2

with open(f_path, encoding='utf-8') as f:
    for line in f:
        for i in range(0,len(titlelist1)):
            key = titlelist1[i]
            if key == (line.split('-')[0]):
                d1.setdefault(key, []).append(line.split('-')[1])
print(d1)