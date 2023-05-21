from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from tree_sitter import Language, Parser
from transformers import RobertaTokenizer, RobertaModel

tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")

# Load the language's grammar
Language.build_library(
  'build/my-languages.so',
  ['vendor/tree-sitter-python', 'vendor/tree-sitter-javascript', 'vendor/tree-sitter-java']
)

PYTHON_LANGUAGE = Language('build/my-languages.so', 'python')
JAVASCRIPT_LANGUAGE = Language('build/my-languages.so', 'javascript')
JAVA_LANGUAGE = Language('build/my-languages.so', 'java')

def parse_code(code, language):
    parser = Parser()
    if language == 'python':
        parser.set_language(PYTHON_LANGUAGE)
    elif language == 'javascript':
        parser.set_language(JAVASCRIPT_LANGUAGE)
    elif language == 'java':
        parser.set_language(JAVA_LANGUAGE)
    else:
        raise ValueError(f'Unsupported language: {language}')

    tree = parser.parse(bytes(code, "utf8"))
    # Now you can analyze the syntax tree

def highlight_code(code, language):
    lexer = get_lexer_by_name(language)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)






def analyze_code(processed_input):
    code = processed_input['code']
    inputs = tokenizer(code, return_tensors="pt")
    outputs = model(**inputs)
    error = processed_input['error']

    # A simple static code analysis: check if the error is in the code
    if error in code:
        return f"The error message '{error}' is found in your code."
    else:
        return f"The error message '{error}' is not found in your code."


from transformers import RobertaTokenizer, RobertaModel

tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")

def analyze_code(code):
    inputs = tokenizer(code, return_tensors="pt")
    outputs = model(**inputs)
    # Now you can use the outputs for further analysis
