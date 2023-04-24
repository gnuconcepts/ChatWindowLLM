from tkinter import *
import openai
import csv
import os
import datetime
import random
import json

def find_value_by_key(csv_filename, key):
    with open(csv_filename,encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['Key'] == key:
                return row['Value'].strip()
    return None

def log(string):
    # Get the current date and time
    now = datetime.datetime.now()

    # Generate a random number between 1 and 1000
    rand_num = random.randint(1, 1000)

    # Format the filename using the current date and time and the random number
    filename = f"log_{now.strftime('%Y%m%d_%H%M%S')}_{rand_num}.txt"

    # Create the logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Open the file in write mode
    with open(f"logs/{filename}", "w") as f:
        # Write the message to the file
        f.write(string + "\n")

def call_gpt(messages):
    #print(messages)
    #return "I don't know"
    new_msg = [{"role": "system", "content": "You are a helpful assistant."}]
    msgs = new_msg + [{"role": role, "content": content} for role, content in messages]
    #msgs = [{"role": role, "content": content} for role, content in messages]
    print(msgs)
    response = call_chatgpt(msgs)
    return response


def call_chatgpt(msgs):
    #print(msgs)
    openai.api_key = find_value_by_key("c:\keystore\Keys.txt", "OPENAI_KEY")
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=msgs
    )

    return response.choices[0].message.content.strip()


root = Tk()
root.title("Let's Chat")

BG_GRAY = "#ABABAB"
BG_COLOR = "#171717"
TEXT_COLOR = "#EAEAEA"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def display_chat_history(txt,chathistory):
    txt.delete("1.0", END)
    log(json.dumps(chathistory))
    for chat in chathistory:
        sender, message = chat
        txt.insert(END, f"{sender}: {message}\n")




# Send function
def send():
	chathistory.append(("user", e.get()))
	user = e.get().lower()
	chathistory.append(("assistant", call_gpt(chathistory)))
	
	display_chat_history(txt,chathistory)
	e.delete(0, END)


lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Let's Chat", font=FONT_BOLD, pady=10, width=20, height=1).grid(
	row=0)

txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)

# Create the scroll bar
scrollbar = Scrollbar(root, command=txt.yview)
scrollbar.grid(row=1, column=2, sticky="nsew")

# Configure the text box to use the scroll bar
txt.configure(yscrollcommand=scrollbar.set)
txt.grid(row=1, column=0,columnspan=2, sticky="nsew")

# Use grid column weights to make the text box and scroll bar resizeable
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)

e = Entry(root, bg="#2C2C2C", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)

sendbtn = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
			command=send).grid(row=2, column=1,columnspan=2)


def func(event):
    print("You hit return.")
    send()
root.bind('<Return>', func)

chathistory = [("assistant","How can I help you?")]
display_chat_history(txt,chathistory)


root.mainloop()
