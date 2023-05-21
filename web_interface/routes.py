from flask import request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from web_interface import app
from web_interface.user_management import load_user, User
from input_processing.input_processor import process_input
from code_analysis.code_analyzer import analyze_code
from solution_generation.solution_generator import generate_solution
from output_processing.output_processor import process_output

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in User.users if user.username == username), None)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    output = None
    if request.method == 'POST':
        try:
            code = request.form['code']
            problem = request.form['problem']
            if not code or not problem:
                raise ValueError("Both code and problem description must be provided.")
            processed_input = process_input(code, problem)
            analysis_result = analyze_code(processed_input)
            solution = generate_solution(analysis_result)
            output = process_output(solution)
        except ValueError as e:
            output = str(e)
        except Exception as e:
            output = "An unexpected error occurred."
    return render_template('index.html', output=output)
