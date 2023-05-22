from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer

from web_interface import app, mail
from web_interface.user_management import load_user, User
from input_processing.input_processor import process_input
from code_analysis.code_analyzer import analyze_code
from solution_generation.solution_generator import generate_solution
from output_processing.output_processor import process_output
from flask_mail import Message
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    mail_subject = 'Activate your account.'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': request.META['HTTP_HOST'],
        'uid': uid,
        'token': token,
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


urlpatterns = [
    path('reset_password/', PasswordResetView.as_view(), name='reset_password')
]


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
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(email, salt='password-reset-salt')
            msg = Message('Password Reset Request', sender='noreply@codecompanion.com', recipients=[email])
            msg.body = f'Click the following link to reset your password: {url_for('reset_password_token', token=token, _external=True)}'
            mail.send(msg)
            flash('A password reset link has been sent to your email.', 'info')
        else:
            flash('No account found with that email.', 'warning')
    return render_template('reset_password_request.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    try:
        email = URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'warning')
        return redirect(url_for('reset_password'))
    user = User.query.filter_by(email=email).first()
    if request.method == 'POST':
        password = request.formI apologize for the cut-off in the previous message. Here's the continuation of the code:

```python
        password_hash = generate_password_hash(password)
        user.password_hash = password_hash
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password_token.html')

@app.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(token, salt='email-verification-salt', max_age=3600)
    except:
        flash('The email verification link is invalid or has expired.', 'warning')
        return redirect(url_for('index'))
    user = User.query.filter_by(email=email).first()
    user.email_verified = True
    db.session.commit()
    flash('Your email has been verified.', 'success')
    return redirect(url_for('index'))

@app.route('/history', methods=['GET'])
@login_required
def history():
    submissions = Submission.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', submissions=submissions)
