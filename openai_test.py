from openai import OpenAI
client = OpenAI()
def caller(prompt) -> None:

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": "create website using python flask main.py using input "
        + "Give file structure with space before file name ex: \"--- filename.html\", file code, README.md Dont explain running input or overview:"
        + prompt}
    ]
    )
    # print(completion.choices[0].message.content)

    with open('input.txt', 'w', encoding="utf-8") as file:
        # file.write("\n\n---------Chat Reponse-----------")
        file.write(str(completion.choices[0].message.content))
        # file.write("\n-----------End of reponse-----------\n")

def tester(filepath, error_code) -> None:
    with open(filepath, 'r', encoding="utf-8") as file:
        file_content = file.read()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content":"Error in\n" + file_content + "\n" + error_code + "give updated code no explanation:"}
    ]    
    )

    with open('outputTest.txt', 'w', encoding="utf-8") as file:
        file.write(str(completion.choices[0].message.content))
    return str(completion.choices[0].message.content)
