import google.generativeai as genai

genai.configure(api_key = '')

model = genai.GenerativeModel("gemini-1.5-flash")
exchange = 'MEXC'

with open('coin-prompt.txt') as f:
    
    prompt = ''.join(f.readlines())

prompt = prompt.replace('||EXCHANGE||', exchange)
messages = []

while True:

    message = input()
    messages.append(message)
    result = model.generate_content(
        [prompt, *messages]
    )
    print(result.text)

