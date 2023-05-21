import openai

openai.api_key = 'sk-APIKEY'

def generate_solution(code, problem):
    prompt = f"{code}\n# Problem: {problem}\n# Solution:"
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.5,
      max_tokens=100
    )
    return response.choices[0].text.strip()
