import csv

x1 = [1, 2]
x2 = [3, 4]
y1 = [5, 6]
y2 = [7, 8]

with open("data.csv", "w", newline='') as f:
    w = csv.writer(f)
    for i1, i2, j1, j2 in zip(x1, x2, y1, y2):
        w.writerow([i1 - i2, j1 - j2])