import json

data = json.load(open("test_dataset.json", "r"))
for key in data:
    items = data[key].items()
    new_value = []
    for item in items:
        item[1]["source"] = item[0]
        new_value.append(item[1])
    data[key] = new_value
    print(data[key])

#print(data)
json.dump(data, open("test_dataset2.json", "w"))
