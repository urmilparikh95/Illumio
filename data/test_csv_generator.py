import csv
import random

output_csv_path = "big.csv"

small_csv_path = "small.csv"
tag_map = {}

with open(small_csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["dstport"], row["protocol"])
        if key not in tag_map:
            tag_map[key] = []
        tag_map[key].append(row["tag"])


fields = ["dstport", "protocol", "tag"]

with open(output_csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for _ in range(10000):
        # 50% chance to use existing patterns, 50% to generate new ones
        if random.random() < 0.5:
            key = random.choice(list(tag_map.keys()))
        else:
            # only use tcp, udp and icmp
            key = (str(random.randint(0, 65535)), random.choice(["1", "6", "17"]))

        dstport, protocol = key
        tag = random.choice(tag_map.get(key, ["sv_P8", "sv_P9", "sv_P10"]))

        writer.writerow({"dstport": dstport, "protocol": protocol, "tag": tag})