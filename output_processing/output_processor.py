from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pylint import epylint as lint
from black import format_str, FileMode

def process_output(solution):
    # Syntax highlight the solution
    highlighted_solution = highlight(solution, PythonLexer(), TerminalFormatter())

    # Analyze the code for errors
    lint_stdout, lint_stderr = lint.py_run(solution, return_std=True)
    error_type, potential_fixes = lint_stderr.getvalue(), lint_stdout.getvalue()

    # Format the code
    formatted_solution = format_str(solution, mode=FileMode())

    # Provide step-by-step instructions
    instructions = "\n".join(f"Step {i+1}: {step}" for i, step in enumerate(formatted_solution.split("\n")))

    # Provide a link to additional resources
    resources = "For more information, visit: https://docs.python.org/3/"

    # Provide error type and potential fixes
    error_info = f"Error Type: {error_type}\nPotential Fixes: {potential_fixes}"

    return f"{highlighted_solution}\n\n{instructions}\n\n{resources}\n\n{error_info}"
