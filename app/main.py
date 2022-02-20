from flask import Flask,render_template_string, flash, request
import pandas as pd
from datetime import datetime

def HtmlIntake(path):
    with open(path) as f:
        lines = f.readlines()
    return ''.join(lines)

def main(homePage, correctPage):
    app = Flask(__name__)

    #  Get question
    today = datetime.today().strftime('%m/%d/%Y')
    df = pd.read_csv("app/static/Caitvia_db.csv")
    try:
        row = df[df['Date'] == today]
        question = row['Question'].values[0]
        answer = row['Answer'].values[0]
    except:
        question = 'Uh Oh- Jack messed something up. Tell him pls'
        answer = 'Uh Oh- Jack messed something up. Tell him pls'

    @app.route("/" , methods=['GET'])
    def launch_hp():
        return render_template_string(homePage.replace('{question_insert}', question))

    @app.route("/userInput", methods=["POST"])
    def result():
        guess = request.form["answer"]
        print(guess)
        if guess.lower() == answer.lower():
            return render_template_string(correctPage.replace('{answer}',answer))
        elif guess.lower() == 'i give up':
            return render_template_string(giveUpPage.replace('{answer}',answer))
        else:
            return render_template_string(incorrectPage)

    app.run()

if __name__ == '__main__':
    homePage = HtmlIntake("app/templates/homePage_fr.html")
    correctPage = HtmlIntake("app/templates/correct.html")
    incorrectPage = HtmlIntake("app/templates/incorrect.html")
    giveUpPage = HtmlIntake("app/templates/giveUpPage.html")
    main(homePage, correctPage)

