import csv
from constants import *
import os

class CSVHelper():
    def __init__(self, filepath, num_images=NUM_IMAGES, questions=QUESTIONS, out_path = None):
        self.filepath = filepath
        self.num_images = num_images
        self.questions = questions
        if not out_path:
            self.outpath = os.path.dirname(self.filepath)
        else:
            self.outpath = out_path
        self.rows = []
        self.fieldnames = []
        self.clean_data = []
        self.clean_fieldnames = CLEAN_FIELDNAMES
        self.get_rows()
        self.get_clean_data()
    
    def get_rows(self):
        inf = open(self.filepath, "r")
        csv_reader = csv.DictReader(inf)
        self.fieldnames = csv_reader.fieldnames
        self.rows = [dict(row) for row in csv_reader]
        inf.close()
    
    def get_clean_data(self):
        input_csv = os.path.splitext(os.path.basename(self.filepath))[0]
        clean_csv_path = os.path.join(self.outpath, input_csv)
        if os.path.exists(clean_csv_path):
            for q in range(len(self.questions)):
                cleanfile = os.path.join(clean_csv_path, f"{input_csv}_question{q + 1}.csv")
                inf = open(cleanfile, "r")
                csv_reader = csv.DictReader(inf)
                self.clean_fieldnames = csv_reader.fieldnames
                self.clean_data.append([dict(row) for row in csv_reader])
                inf.close()
        else:
            output_fieldnames = CLEAN_FIELDNAMES
            os.makedirs(clean_csv_path)
            for q in range(len(self.questions)):
                cur_question = []
                cleanfile = os.path.join(clean_csv_path, f"{input_csv}_question{q + 1}.csv")
                outf = open(cleanfile, "w")
                csv_writer = csv.DictWriter(outf, output_fieldnames)
                csv_writer.writeheader()
                for image in range(self.num_images):
                    cur_row = {}
                    for fieldname in output_fieldnames:
                        if fieldname.startswith("des"):
                            num = int(fieldname[3:])
                            cur_row[fieldname] = self.rows[num][f"Answer.question{q + 1}_{image + 1}"]
                        elif fieldname == "ground_truth":
                            cur_row[fieldname] = self.rows[0][f"Input.attack_id_full_{image}"][:-4]
                        elif fieldname.startswith("status"):
                            cur_row[fieldname] = ""
                        else:
                            cur_row[fieldname] = self.rows[0][f"Input.{fieldname}_{image}"]
                    csv_writer.writerow(cur_row)
                    cur_question.append(cur_row)
                outf.close()
                self.clean_data.append(cur_question)

    
    def get_info(self):
        result = {
            'images': [],
        }
        for image_number in range(self.num_images):
            image_result = {
                'url': self.rows[0][f'Input.url_{image_number+1}'],
                'questions': []
            }
            for question_number, question_text in enumerate(self.questions):
                question = {}
                question['question'] = question_text
                question['answers'] = []
                for answer_number, row in enumerate(self.rows):
                    answer_state = 'unanswered'
                    if self.clean_data[question_number][image_number][f"status des{answer_number}"] == "accept":
                        answer_state = 'accept'
                    elif self.clean_data[question_number][image_number][f"status des{answer_number}"] == "reject":
                        answer_state = 'reject'
                    question['answers'].append({
                        'responder_id': row['WorkerId'],
                        'answer': row[f'Answer.question{question_number + 1}_{image_number + 1}'],
                        'id': f'{image_number + 1}_{question_number + 1}_{answer_number + 1}',
                        'state': answer_state
                    })
                image_result['questions'].append(question)
            result['images'].append(image_result)
        return result
    
    def write_results(self, results):
        num_rows = len(self.rows)
        image_results = {
            self.rows[0][f'Input.url_{image_number+1}'] : [[0,0,0] for _ in self.questions]
            for image_number in range(self.num_images)}
        worker_results = {answer_number: 0 for answer_number in range(num_rows)}
        for key in results:
            image_number, question_number, answer_number = [int(s) for s in key.split('_')]
            if results[key][0] == "reject":
                image_results[self.rows[0][f'Input.url_{image_number}']][question_number - 1][2] += 1
                self.clean_data[question_number - 1][image_number - 1][f"status des{answer_number - 1}"] = 'reject'
            else:
                image_results[self.rows[0][f'Input.url_{image_number}']][question_number - 1][1] += 1
                worker_results[answer_number - 1] += 1
                self.clean_data[question_number - 1][image_number - 1][f"status des{answer_number - 1}"] = 'accept'
            image_results[self.rows[0][f'Input.url_{image_number}']][question_number - 1][0] += 1

        for answer_number in range(num_rows):
            if (worker_results[answer_number] < (0.75 * self.num_images * len(self.questions))): 
                self.rows[answer_number]["Reject"] = "x"
                self.rows[answer_number]["Approve"] = ""
            else:
                self.rows[answer_number]["Reject"] = ""
                self.rows[answer_number]["Approve"] = "x"
        
        self.write_csv()
        return image_results

    

    def write_csv(self):
        input_csv = os.path.splitext(os.path.basename(self.filepath))[0]
        clean_csv_path = os.path.join(self.outpath, input_csv)
        if not os.path.exists(clean_csv_path):
            os.makedirs(clean_csv_path)
        output_csv_path = os.path.join(clean_csv_path, "upload.csv")
        outf = open(output_csv_path, "w")
        csv_writer = csv.DictWriter(outf, self.fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(self.rows)
        outf.close()

        for q, question_data in enumerate(self.clean_data):
            cleanfile = os.path.join(clean_csv_path, f"{input_csv}_question{q + 1}.csv")
            outf = open(cleanfile, "w")
            csv_writer = csv.DictWriter(outf, self.clean_fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(question_data)
            outf.close()
        






            
