import logging
from input_processing.input_processor import process_input
from code_analysis.code_analyzer import analyze_code
from solution_generation.solution_generator import generate_solution
from output_processing.output_processor import process_output

def main():
    logging.basicConfig(filename='codecompanion.log', level=logging.DEBUG)
    try:
        processed_input = process_input()
    except Exception as e:
        logging.error(f"Error in input processing: {str(e)}")
        print("An error occurred while processing the input.")
        return

    try:
        analysis_result = analyze_code(processed_input)
    except Exception as e:
        logging.error(f"Error in code analysis: {str(e)}")
        print("An error occurred while analyzing the code.")
        return

    try:
        solution = generate_solution(analysis_result)
    except Exception as e:
        logging.error(f"Error in solution generation: {str(e)}")
        print("An error occurred while generating the solution.")
        return

    try:
        output = process_output(solution)
        print(output)
    except Exception as e:
        logging.error(f"Error in output processing: {str(e)}")
        print("An error occurred while processing the output.")

if __name__ == "__main__":
    main()

    
