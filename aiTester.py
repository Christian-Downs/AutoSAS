from openai import OpenAI
client = OpenAI()
def caller(prompt) -> None:

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": "create website using python flask main.py using input "
        + "Give file structure, file code, README.md Dont explain running input or overview:"
        + prompt}
    ]
    )
    # print(completion.choices[0].message.content)

    with open('input.txt', 'w', encoding="utf-8") as file:
        # file.write("\n\n---------Chat Reponse-----------")
        file.write(str(completion.choices[0].message.content))
        # file.write("\n-----------End of reponse-----------\n")