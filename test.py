import json
data = json.load(open('test.json',"r"))
print(data)
data = json.dump(["a"], open('test.json',"w"))
print(data)
