import csv

def create_batch(file_path,output_file_path,batch_size = 10):
    inf = open(file_path, "r")
    csv_reader = csv.DictReader(inf)
    fieldnames = csv_reader.fieldnames
    rows = [dict(row) for row in csv_reader]
    inf.close()
    outf = open(output_file_path, "w")
    output_fieldnames = []
    for fieldname in fieldnames:
        for i in range(batch_size):
            output_fieldnames.append(f"{fieldname}_{i+1}")
    csv_writer = csv.DictWriter(outf, output_fieldnames)
    csv_writer.writeheader()
    for i in range(0,len(rows),batch_size):
        curr_row = {}
        for j in range(batch_size):
            if (i + j) >= len(rows):
                break
            for fieldname in fieldnames:
                curr_row[f"{fieldname}_{j+1}"] = rows[i + j][fieldname]
        csv_writer.writerow(curr_row)
    outf.close()

create_batch(file_path="./AMT_BATCHES/batch_0.csv", output_file_path="./test_batch.csv")