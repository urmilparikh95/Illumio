import random


if __name__ == '__main__':
    num_rows = 5
    num_cols = 3
    data = []
    for _ in range(50000):
        row = []
        row.append("2")
        row.append("123456789012")
        row.append("eni-0a1b2c3d")
        row.append("10.0.1.201")
        row.append("198.51.100.2")
        row.append(str(random.randint(0, 65535)))
        row.append(random.choice([str(random.randint(0, 1024)), str(random.randint(1025, 65535))]))
        row.append(random.choice(["1", "6", "17"]))
        row.append("25")
        row.append("20000")
        row.append("1620140761")
        row.append("1620140821")
        row.append("ACCEPT")
        row.append("OK")
        data.append(row)

    with open('big.log', 'w') as f:
        for row in data:
            f.write(' '.join(row) + '\n')
    