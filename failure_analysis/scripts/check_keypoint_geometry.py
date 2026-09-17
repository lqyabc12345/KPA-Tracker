import json


ann_path = (
"dataset1/laptop/train/00007/annotations/00231.json"
)


with open(ann_path,"r") as f:
    data=json.load(f)


print(data.keys())


instance=data["instances"][0]


print(instance.keys())


print("number links:",
      len(instance["links"]))


for link in instance["links"]:

    print(
        link.keys()
    )