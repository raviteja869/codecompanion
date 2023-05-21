from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pylint import epylint as lint
from transformers import RobertaTokenizer, RobertaModel

tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")


def analyze_code(code, language):
    inputs = tokenizer(code, return_tensors="pt")
    outputs = model(**inputs)

    if language == 'python':
        (pylint_stdout, pylint_stderr) = lint.py_run(code, return_std=True)
        pylint_output = pylint_stdout.getvalue()
        return pylint_output
    else:
        raise ValueError(f'Unsupported language: {language}')


def highlight_code(code, language):
    lexer = get_lexer_by_name(language)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)
