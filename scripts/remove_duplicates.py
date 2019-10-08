import csv

data_in = "../good_reads_final.csv"
data_out = "../dataset.csv"

with open(data_in, 'r', newline='') as in_file, open(data_out, 'w', newline='') as out_file:
    reader = csv.reader(in_file)
    writer = csv.writer(out_file)
    seen = set() # set for fast O(1) amortized lookup
    for row in reader:
        row = tuple(row)
        if row[11] in seen: continue # skip duplicate
        seen.add(row[11]) #row[11] is book_id
        writer.writerow(row)