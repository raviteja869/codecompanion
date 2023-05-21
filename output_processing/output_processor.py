from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

def process_output(solution):
    # Syntax highlight the solution
    highlighted_solution = highlight(solution, PythonLexer(), TerminalFormatter())

    # Provide step-by-step instructions
    instructions = "\n".join(f"Step {i+1}: {step}" for i, step in enumerate(solution.split("\n")))

    # Provide a link to additional resources
    resources = "For more information, visit: https://docs.python.org/3/"

    return f"{highlighted_solution}\n\n{instructions}\n\n{resources}"
