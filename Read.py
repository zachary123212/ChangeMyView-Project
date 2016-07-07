import json

data = []

with open("train_pair_data.jsonlist", "r") as raw:
    for line in raw.readlines():
        data.append(json.loads(line))

# for item in data:
#     print(item["op_title"])

print(data[0].keys())
print(data[0]['positive'].keys())
print(data[0]['positive']['comments'][0]['body'])
