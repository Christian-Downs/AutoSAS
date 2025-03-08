from openai import OpenAI


userInput = "I need a file to store employee info"
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "create website using python flask main.py using input "
    + "Give file structure, file code, README.md Dont explain running input or overview:"
    + userInput}
  ]
)

print(completion.choices[0].message.content)

with open('output.txt', 'a', encoding="utf-8") as file:
    file.write("\n\n---------Chat Reponse-----------")
    file.write(str(completion.choices[0].message.content))
    file.write("\n-----------End of reponse-----------\n")