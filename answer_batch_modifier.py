import csv

NUM_IMAGES = 10
NUM_QUESTIONS = 2 

def create_answer_batch(file_path,output_file_path, num_images = NUM_IMAGES, num_questions = NUM_QUESTIONS):
    inf = open(file_path, "r")
    csv_reader = csv.DictReader(inf)
    fieldnames = csv_reader.fieldnames
    rows = [dict(row) for row in csv_reader]
    inf.close()    
    output_fieldnames = ["transaction_id", "trial_id", "trial_name", "ground_truth", "des0","des1","des2","des3","des4"]
    for question in range(num_questions):
        outf = open(output_file_path + f"_question{question + 1}.csv", "w")
        csv_writer = csv.DictWriter(outf, output_fieldnames)
        csv_writer.writeheader()
        for image in range(num_images):
            cur_row = {}
            for fieldname in output_fieldnames:
                if fieldname.startswith("des"):
                    num = int(fieldname[3:])
                    print(fieldname)
                    print(rows[num][f"Answer.question{question + 1}_{image + 1}"][:50])
                    cur_row[fieldname] = rows[num][f"Answer.question{question + 1}_{image + 1}"]
                elif fieldname == "ground_truth":
                    cur_row[fieldname] = rows[0][f"Input.attack_id_full_{image}"][:-4]
                else:
                    cur_row[fieldname] = rows[0][f"Input.{fieldname}_{image}"]
            csv_writer.writerow(cur_row)
        outf.close()

create_answer_batch(file_path="./AMT_ANSWERS/batch1_cropped.csv", output_file_path="./AMT_ANSWERS_CLEANED/batch1_cropped")