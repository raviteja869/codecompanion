from input_processing.input_processor import process_input
from code_analysis.code_analyzer import analyze_code
from solution_generation.solution_generator import generate_solution
from output_processing.output_processor import process_output

def main():
    try:
        processed_input = process_input()
        analysis_result = analyze_code(processed_input)
        solution = generate_solution(analysis_result)
        output = process_output(solution)
        print(output)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
