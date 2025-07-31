from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus,
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.ImageGeneration import GenerateImages

from dotenv import dotenv_values
from asyncio import run
from time import sleep
import threading
import json
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

# Default conversation message
DefaultMessage = f'''{Username}: Hello {Assistantname}, How are you?\n\n{Assistantname}: Welcome {Username}. I am doing well. How may I help you?'''

Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Ensure necessary file/folder exists
def EnsureDataFiles():
    os.makedirs("Data", exist_ok=True)
    chatlog_path = r'Data\ChatLog.json'
    if not os.path.exists(chatlog_path):
        with open(chatlog_path, 'w', encoding='utf-8') as f:
            json.dump([], f)

# Set default chat if nothing is found
def ShowDefaultChatIfNoChats():
    with open(r'Data\ChatLog.json', "r", encoding='utf-8') as File:
        if len(File.read()) < 5:
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                file.write("")
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
                file.write(DefaultMessage)

# Read previous chats
def ReadChatLogJson():
    with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Update chat log to GUI-readable format
def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

# Show chat text on GUI
def ShowChatsOnGUI():
    with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as File:
        Data = File.read()

    if len(Data) > 0:
        with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as File:
            File.write('\n'.join(Data.split('\n')))

# Runs before GUI starts
def InitialExecution():
    EnsureDataFiles()
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

# Main logic thread
def MainExecution():
    TaskExecution = False
    ImageExecution = False

    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")

    Decision = FirstLayerDMM(Query)
    print(f"\nDecision: {Decision}\n")

    G = any(i.startswith("general") for i in Decision)
    R = any(i.startswith("realtime") for i in Decision)

    Mearged_query = " and ".join(
        ["".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    # ✅ Check for automation commands
    for queries in Decision:
        if not TaskExecution and any(queries.startswith(func) for func in Functions):
            run(Automation(Decision))
            TaskExecution = True

    # ✅ Check for image generation
    for queries in Decision:
        if "generate" in queries and "image" in queries:
            try:
                # ✅ Extract prompt cleanly
                prompt = Query.lower()
                prompt = prompt.replace("generate", "").replace("an", "").replace("a", "")
                prompt = prompt.replace("the", "").replace("image", "").strip().capitalize()

                if not prompt:
                    prompt = "random futuristic landscape"  # fallback default prompt

                SetAssistantStatus("Creating image...")
                ShowTextToScreen(f"{Assistantname}: Generating image for '{prompt}'")
                GenerateImages(prompt)
                SetAssistantStatus("Answering...")
                TextToSpeech(f"Here is the image of {prompt}")
                return True
            except Exception as e:
                print(f"[MainExecution] Image generation error: {e}")
                ShowTextToScreen(f"{Assistantname}: Sorry, I couldn't generate the image.")
                return True

    if G and R or R:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        return True

    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True

            elif "realtime" in Queries:
                SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True

            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                os._exit(1)


# Thread 1: Background logic
def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." not in AIStatus:
                SetAssistantStatus("Available...")
            sleep(0.1)

# Thread 2: GUI
def SecondThread():
    GraphicalUserInterface()

# Start Threads
if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
