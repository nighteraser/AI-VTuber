from openai import OpenAI
import prompt_maker
import json

# Ollama
MODEL = 'mistral' # for ollama
client = OpenAI(base_url='http://localhost:11434/v1/', api_key='ollama')

# LM studio
# MODEL = 'TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q2_K.gguf' # for LM studio
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def load_history_conversation():
    with open("conversation.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["history"]

def get_ai_answer(user_query_text):

    conversation = load_history_conversation()

    total_chars = sum(len(d['content']) for d in conversation)
    while total_chars > 4000:
        try:
            conversation.pop(2)
            total_chars = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error removing old messages: {0}".format(e))

    conversation.append({'role': 'user', 'content': user_query_text})

    prompt = prompt_maker.get_prompt()
    prompt.append({'role': 'user', 'content': user_query_text})

    chat_completion = client.chat.completions.create(
        model=MODEL,
        messages=prompt,
        temperature=0.9, # high temperature more creative
    )

    message = chat_completion.choices[0].message.content
    conversation.append({'role': 'assistant', 'content': message})
    
    history = {"history": conversation}
    # Store all history conversation to conversation.json
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    return message


