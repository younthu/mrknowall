from flask import Flask, request
from flask import render_template
import sys
import os
# sys.path.append(os.path.abspath("./"))
sys.path.append("..")
# from oracles.gender_detector import GenderDetector
from oracles.GenderDetector import GenderDetector

app = Flask(__name__, static_folder='templates', static_url_path='')

@app.route("/")
def hello():
    return render_template('index.html',gender='',name='')

@app.route("/gender")
def gender():
    f,m,r = GenderDetector.load_from_file('name_gender.bin').detect(request.args.get('name'))

    print(f,m,r)
    if f ==0 and m == 0:
        guessed_gender = '不确定'
    elif r > 0.5:
        guessed_gender = '女生'
    else:
        guessed_gender = '男生'

    return render_template('index.html',name=request.args.get('name'),gender=guessed_gender)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)