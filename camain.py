from llama_cpp import Llama
import discord
import os

token = ""

intents = discord.Intents.default()
client = discord.Client(intents=intents)

llm = Llama(model_path="Truthful_DPO_TomGrc_FusionNet_7Bx2_MoE_13B-Q5_1.gguf", n_ctx=2048, verbose=False,n_threads=20, n_threads_batch=20)
what = ""
before = ""
System = "Act like you were a Sentient being called Sage."

if os.path.isfile('saved_list.txt'):
    with open('saved_list.txt', 'r', encoding='utf-8') as file:
        liste = file.readlines()
        liste = [line.strip() for line in liste]
else:
    liste = [System]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        global System
        prompt = message.content
        if prompt[0] == "<":
            prompt = prompt[23:]
        channel = message.channel
        user_name = message.author.name
        if "forgor" in prompt:
            with open ("brain.txt", "w", encoding="utf-8") as file:
                file.write("")
            with open ("brain.txt", "w", encoding="utf-8") as file:
                file.write("")
            return

        with open("brain.txt", "r", encoding="utf-8") as file:
            all = file.read()

        with open("prompt.txt","r", encoding="utf-8") as file:
            System = file.read()

        what = f"{System}\\n{all}\\n{user_name}: {prompt}\\nSmuggy: "
        output = llm(f"{what}", max_tokens=512, echo=False) #["Q:", "\n"]
        await channel.send(output['choices'][0]['text'])

        liste.append(f"{user_name}: {prompt}")
        liste.append(f"Smuggy: {output['choices'][0]['text']}")

        if len(liste) >= 10:
            del liste[0]
            del liste[0]
            del liste[0]
        with open("brain.txt", "w") as file:
            file.write("")
        with open("brain.txt", "w", encoding="utf-8") as file:
            for x in liste:
                file.write(f"{x}\n")

        with open('saved_list.txt', 'w', encoding='utf-8') as file:
            for item in liste:
                file.write(f"{item}\n")

        System = ""


client.run(token)