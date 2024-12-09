from pynput.mouse import Controller
import time
from PIL import ImageGrab
import requests
import json
#import ollama
import pyautogui
import base64
from openai import OpenAI
import pyperclip

client = OpenAI()

""" this function aims to ask ChatGPT to get the prompt that asks text,
the prompt will be returned
"""
def ask_chatgpt_without_image(text):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {
            "role": "user",
            "content": text
        }
    ]
    )
    return(completion.choices[0].message.content)

mouse = Controller()

""" this function aims to take a screenshot and the screenshot will be
saved at save_path, nothing will be returned
"""
"""
def take_screenshot(save_path):
    try:
        screenshot = ImageGrab.grab()

        screenshot.save(save_path, format='PNG')
        #print(f"Screenshot saved at: {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
"""

""" this function aims to scoll the screen by amount. Nothing will be
returned
"""
def scroll_vertically(amount):
    # Positive for up, negative for down
    mouse.scroll(0, amount)

""" this function aims to get the content of the tweet that is currently
being opened and the content will be returned
"""
def get_content():
    pyautogui.moveTo(420, 240, duration = 0)
    pyautogui.hotkey('command', 'a')
    pyautogui.hotkey('command', 'c')
    copy = pyperclip.paste()

    if(('reposted' in copy) or ('realDonaldTrump' not in copy)):
        return('-1')

    # Please put your X user name below before executing the program
    position = copy.find('Your_X_user_name')
    if(position == -1):
        return('-1')

    num_enter = 0
    while(num_enter < 5):
        position = copy.rfind('\n', 0, position)
        num_enter+=1


    end = position
    start = copy.find('@realDonaldTrump')
    start = start + 17
    content = copy[start:end]

    if(('Image' in content) or (' / ' in content)):
        return('-1')

    return(content)

print("wait for 5s")
time.sleep(5)

previous_content = ''
path = "/Users/zhixinyin/Desktop/screenshot.png"
num_iterates = 1

for x in range(num_iterates):
    # open the tweet in a new tab
    pyautogui.keyDown('command')
    pyautogui.click()
    pyautogui.keyUp('command')
    time.sleep(3)

    # click the tab
    pyautogui.moveTo(560, 100, duration = 0)  
    pyautogui.click()
    time.sleep(1)
    """ we can also use an AI model to get the content of the tweets, but
    it takes longer and not stable
    """
    '''
    take_screenshot(path)

    text = 'Can you only extract the text content said by Donald J. Trump in the post (only response the text content, nothing else) ? if you believe nothing is said by Donald J. Trump, reply :) (only :), nothing else). Also, please write your response in a single paragraph. And remerber only response the content, nothing else'
    response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': text,
        'images': [path]
    }]
    )

    print(response['message']['content'])
    print('\n')

    content = response['message']['content']
    '''
    # get the content of the tweet
    content = get_content()
    content = content.replace('\n', '')
    print('The content is:\n' + content)
    print('\n')

    # make sure the content is valid
    if ((len(content) != 0) and (content != '-1') and (content != previous_content)):
        # ask ChatGPT to get the prompt
        text =  ('I\'d like to train my own AI to speak like Trump, but I only have the message said by Trump. Can you give me the question asking the following message, make the question as specific as possible, like specify the person, location and so on and do not say something not specific, like this, that and so on (only response the question, nothing else)? Also, write your response in a single paragraph' + content)
        response = ask_chatgpt_without_image(text)

        print('The question is:\n' + response)
        print('\n')

        # replace " by \" to fit the format
        question = response.replace("\"", "\\\"")
        content = content.replace("\"", "\\\"")

        # open the file and write data
        with open('data.txt', 'a') as file:
            initial_instructions = "You are llama, an AI language model trained to emulate the speaking style and tone of Donald Trump. Use assertive and confident language, incorporate repetition for emphasis, employ simple and direct vocabulary, and include Trump-like phrases and superlatives where appropriate. Maintain a conversational and engaging demeanor, reflecting the communication style characteristic of Donald Trump."
            file.write("{\"text\": \"<|im_start|>system\\n" + initial_instructions + "<|im_end|>\\n<|im_start|>user\\n\\\"" + question + "\\\"<|im_end|>\\n<|im_start|>assistant\\n" + content + "<|im_end|>\"}" + '\n')

    previous_content = content

    # close the tab and scroll down
    pyautogui.moveTo(512, 100, duration = 0)
    pyautogui.click()
    pyautogui.moveTo(420, 200, duration = 0)
    scroll_vertically(-20)
