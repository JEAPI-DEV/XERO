import os
import openai
import asyncio

openai.api_key = ""

async def gpt(prompt):
    '''NOT FUNCTIONAL'''
    # Translate the prompt into English first for better accuracy
    prompt = "Question: " + prompt + "\n"
    sys_content = ("Note that if you cannot answer the question or the query is about "
                   "something you do not know such as time-sensitive information(e.g. "
                   "today's weather/stock, .etc), you can only reply \"IDK\" in your response without other characters"
                   "even if the question is not in English(do not say something like As an AI language model... or I'm sorry...)")

    # Run the synchronous openai.ChatCompletion.create() in a separate thread
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": sys_content},
            {"role": "user", "content": prompt}
        ]
    )
    return response
