import json
from constants import *

class SummaryHelper():
    def __init__(self,summary_path, questions=QUESTIONS):
        self.summary_path = summary_path
        with open(summary_path,'r') as f:
            self.summary = json.load(f)
        self.questions = questions


    def update_summary(self, results):
        for image in results:
            if image not in self.summary:
                self.summary[image] = [[0,0,0] for _ in self.questions]
            for question in range(len(results[image])):
                self.summary[image][question][0] += results[image][question][0]
                self.summary[image][question][1] += results[image][question][1]
                self.summary[image][question][2] += results[image][question][2]
        with open(self.summary_path,'w') as f:
            json.dump(self.summary, f)
        