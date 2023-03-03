from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretSurv23"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
# this list will be used to store the user's responses to the survey.

@app.route('/')
def home_page():
    return render_template('survey_start.html', survey=satisfaction_survey)
# render the survey_start.html template, passing in the satisfaction_survey object

@app.route('/start', methods=['POST'])
def start_survey():
    responses.clear()
    return redirect('/questions/0')
# user submits the form on the survey start page, this function is called, which clears the responses list and redirects the user to the first question

@app.route('/questions/<int:question_num>')
def show_question(question_num):
    if question_num != len(responses):
        flash('Invalid question!')
        return redirect(f'/questions/{len(responses)}')
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    
    question = satisfaction_survey.questions[question_num]
    return render_template('question.html', question=question)
# route handles displaying each question in the survey
# If the question_num is not the next question, it flashes an error message and redirects to the next question.
# If all the questions have been answered, it redirects to the completion page.
# The question is passed to the rendered HTML template called question.html

@app.route('/answer', methods=['POST'])
def handle_question():
    answer = request.form['answer']
    responses.append(answer)
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    
    return redirect(f'/questions/{len(responses)}')
# set up a Flask route that handles the submitted answer to a question
# It adds the answer to the responses list and redirects to the next question.
# If all the questions have been answered, it redirects to the completion page.

@app.route('/complete')
def complete():
    return render_template('completion.html')
# Setting up a Flask route that displays the completion page