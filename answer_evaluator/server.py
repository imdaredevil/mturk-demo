from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import sys
from csv_helper import CSVHelper
from summary_helper import SummaryHelper


app = Flask("isi-answer-evaluator")
app.secret_key = 'secretkey'	

csv_helper = None
summary_helper = None


@app.route('/')
def index():
    info = csv_helper.get_info()
    return render_template("home.html",info = info)


@app.route('/submit', methods=["POST"])
def submit():
    results = request.form.to_dict(flat=False)
    summary = csv_helper.write_results(results)
    summary_helper.update_summary(summary)
    return render_template("summary.html",summary = list(summary.items()))



if __name__ == "__main__":
    if (len(sys.argv) <= 2):
        print("Give csv input path, output path and summary path as path parameter")
        sys.exit(-1)
    csv_helper = CSVHelper(sys.argv[1], out_path=sys.argv[2])
    summary_helper = SummaryHelper(sys.argv[3])
    app.secret_key = 'secretkey'	
    app.run(debug=True)