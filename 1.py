import json

list = [{"city":"南平","name":"武夷山"}]

with open("1.txt","w",encoding='utf-8') as f:
    f.write(json.dumps(list,ensure_ascii=False))