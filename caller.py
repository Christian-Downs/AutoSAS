from openai import OpenAI
client = OpenAI()



def caller(prompt, system = None):
    messages = [
        {"role": "user", 
         "content": "create website using python flask main.py using input "
            + "Give file structure, file code, README.md Dont explain running input or overview:"
            + prompt}
    ]

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages= messages,
    response_format={
        "type": "text"
    },
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    with open("output.txt", 'a') as file:
        file.write(str(response.choices[0].message.content))
    return response.choices[0].message.content


