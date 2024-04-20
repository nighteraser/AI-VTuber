import json
import sys

CHARACTER_PATH = './character.txt'
OUTPUT_NUM = 50

def get_identity(character_path):  
    with open(character_path, "r", encoding="utf-8") as f:
        identity_context = f.read()
    return {"role": "user", "content": identity_context}

def get_prompt():
    # total_len = 0
    prompt = []
    prompt.append(get_identity(CHARACTER_PATH))

    with open("./conversation.json", "r") as f:
        data = json.load(f)
    history = data["history"]

    if len(history) == 0:
        print("No history...\n")
        return []
    
    prompt.append({"role": "system", "content": f"Below is conversation history.\n"})

    for message in history[:-1]:
        prompt.append(message)

    prompt.append(
        {
            "role": "system",
            "content": f"Here is the latest conversation.\nMake sure your response is within {OUTPUT_NUM} characters!\n",
        }
    )
    # prompt.append(history[-1])

    return prompt

if __name__ == "__main__":
    prompt = get_prompt()
    print(prompt)
    print(len(prompt))