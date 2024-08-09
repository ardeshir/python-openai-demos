import os

import azure.identity
import openai
from dotenv import load_dotenv
from utils.func import write_to_file, append_to_file

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
elif API_HOST == "ollama":
    client = openai.OpenAI(
        base_url=os.getenv("OLLAMA_ENDPOINT"),
        api_key="nokeyneeded",
    )
    MODEL_NAME = os.getenv("OLLAMA_MODEL")
elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    MODEL_NAME = os.getenv("GITHUB_MODEL")
else:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
    MODEL_NAME = os.getenv("OPENAI_MODEL")


# Important variables 
fileNameMD = "latest.md"
syscontent = "You are a helpful coding assistant that develops solutions and provides references for support."
usercontent = "Write a simple Rust Server that can server MarkDown files from wwwroot directory, and a Dockerfile to run this program?"

messages = [
    {"role": "system", "content": syscontent},
]

if os.path.exists(fileNameMD):
    append_to_file(f'\n\n\n #### {syscontent} \n\n')
else:
    write_to_file(f'### {syscontent} \n\n')

while True:
    question = input("\nYour question: ")
    print("Sending question...")
    append_to_file(question)

    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=1,
        max_tokens=400,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=True,
    )

    print("\nAnswer: ")
    bot_response = ""
    for event in response:
        if event.choices and event.choices[0].delta.content:
            content = event.choices[0].delta.content
            print(content, end="", flush=True)
            append_to_file(content)
            bot_response += content
    print("\n")
    messages.append({"role": "assistant", "content": bot_response})
