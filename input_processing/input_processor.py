import json
import ast

def parse_input(input_string):
    return json.loads(input_string)



def is_valid_python(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False



def get_user_input():
    # This function retrieves the user's input.
    # For now, we'll just return a hardcoded JSON string.
    input_string = '''
    {
      "language": "Python",
      "framework": "Flask",
      "code": "from flask import Flask, request\\napp = Flask(__name__)\\n\\n@app.route('/register', methods=['POST'])\\ndef register():\\n    username = request.form['username']\\n    password = request.form['password']\\n    # Registration logic here\\n    return 'User registered'",
      "error": "KeyError: 'username'",
      "expected_behavior": "The route should take a username and password from the form data and register the user.",
      "actual_behavior": "It's throwing a KeyError.",
      "user_attempts": "Checking the form data."
    }
    '''
    try:
        json.loads(input_string)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON string")
    return input_string


'''
'''

def extract_key_info(input_dict):
    language = input_dict.get('language')
    framework = input_dict.get('framework')
    code = input_dict.get('code')
    error = input_dict.get('error')
    expected_behavior = input_dict.get('expected_behavior')
    actual_behavior = input_dict.get('actual_behavior')
    user_attempts = input_dict.get('user_attempts')

    return language, framework, code, error, expected_behavior, actual_behavior, user_attempts

'''In this step, we'll prepare the extracted information for further analysis. 
For this example, we'll assume that no additional processing is needed and we'll just package the information into a new dictionary.'''
def prepare_for_analysis(language, framework, code, error, expected_behavior, actual_behavior, user_attempts):
    return {
        'language': language,
        'framework': framework,
        'code': code,
        'error': error,
        'expected_behavior': expected_behavior,
        'actual_behavior': actual_behavior,
        'user_attempts': user_attempts
    }


'''
Step 5: Return the Processed Input

We'll add error handling to ensure that each step of the process completes successfully. 
If any step fails, we'll catch the error and raise an appropriate error.
'''

def process_input():
    try:
        input_string = get_user_input()
        input_dict = parse_input(input_string)
        if not is_valid_python(input_dict.get('code')):
            raise ValueError("Invalid Python code")
        key_info = extract_key_info(input_dict)
        processed_input = prepare_for_analysis(*key_info)
    except Exception as e:
        raise RuntimeError("Failed to process input") from e
    return processed_input




