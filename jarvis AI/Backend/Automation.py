from AppOpener import close, open as appopen # Import functions to open and close apps.
from webbrowser import open as webopen #Import web browser functionality
from pywhatkit import search, playonyt #Import functions for Google search and YouTube playback.
from dotenv import dotenv_values # Import doteny to manage environment variables.
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML content.
from rich import print #Import rich for styled console output.
from groq import Groq # Import Groq for Al chat functionalities.
import webbrowser # Import webbrowser for opening URLs.
import subprocess # Import subprocess for interacting with the system.
import requests #Import requests for making HTTP requests.
import keyboard # Import keyboard for keyboard-related actions.
import asyncio #Import asyncio for asynchronous programming.
import os # Import os for operating system functionalities.

env_vars = dotenv_values(".env")

GroqAPIKey = env_vars.get("GroqAPIKey") # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content.

"tw-Data-text tw-text-small tw-ta",

classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
       "tw-Data-text tw-text-small tw-ta",
        "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table",
        "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

#Define a user-agent for making web requests.

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

#Initialize the Groq client with the API key.

client = Groq(api_key=GroqAPIKey)
professional_responses = [

"Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",

"I'm at your service for any additional questions or support you may need-don't hesitate to ask.",

]

#List to store chatbot messages.

messages = []

#System message to provide context to the chatbot.

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ ['Username']}, You're a content writer. You have to write . You can to write content like letter ,codes , applicaton , essays , notes,songs,poems etc."}]

#Function to perform a Google search.

def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a Google search.
    return True # Indicate success.

# Function to generate content using AI and save it to a file.

def Content(Topic):
    def OpenNotepad (File):
        default_text_editor = 'notepad.exe' # Default text editor.
        subprocess. Popen([default_text_editor, File]) # Open the file in Notepad.

#Nested function to generate content using the AI chatbot.

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content":f"{prompt}"})


        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768", # Specify the Al model.
            messages=SystemChatBot + messages, #Include system instructions and chat history.
            max_tokens=2048, #Limit the maximum tokens in the response.
            temperature=0.7, # Adjust response randomness.
            top_p=1, # Use nucleus sampling for response diversity.
            stream=True, # Enable streaming response.
            stop=None #Allow the model to determine stopping conditions.
        )
        Answer ="" # Initialize an empty string for the response.

#Process streamed response chunks.

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic: str = Topic.replace("Content", "")
    ContentByAI = ContentWriterAI (Topic) # Generate content using ar
    with open(rF"Data\{Topic.lower().replace('','')}.txt", "w", encoding="utf-8") as file :
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace('','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    from urllib.parse import quote_plus

    app_name = app.strip().upper()
    print(f"🚀 Trying to open {app_name} using AppOpener...")

    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"❌ {app_name} NOT FOUND... Searching on Google.")

        # Generate a Google search query
        query = f"{app} site:{'https://www.' + app.lower() + '.com'}"
        search_url = f"https://www.google.com/search?q={quote_plus(query)}"
        
        try:
            response = sess.get(search_url, headers={"User-Agent": useragent})
            soup = BeautifulSoup(response.text, "html.parser")
            link_tag = soup.find("a", href=True)

            # Attempt to open first valid link
            if link_tag:
                href = link_tag['href']
                if "url?q=" in href:
                    link = href.split("url?q=")[1].split("&")[0]
                    if link.startswith("http"):
                        webopen(link)
                        print(f"✅ OPENED {app_name} via Google.")
                        return True

            # Fallback to YouTube or generic search
            webopen(f"https://www.google.com/search?q={quote_plus(app)}")
            print(f"✅ OPENED {app_name} via Google (Fallback).")
            return True

        except Exception as e:
            print(f"❌ Failed to open {app_name}. Reason: {str(e)}")
            return False

def CloseApp(app):
    if "chrome" in app:
        pass #Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True 

        except:
            return False 


def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    def unmute():
        keyboard.press_and_release("volume unmute")
    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True   

async def TranslateAndExecute(commands: list[str]):
    funcs = []  # List to store asynchronous tasks.
    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            elif "open file" == command:
                pass    
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open").strip())
                funcs.append(fun)

        elif command.startswith("general"):  # Placeholder for general commands.
            pass
        elif command.startswith("realtime"):  # Placeholder for real-time commands. 
            pass
        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close").strip())
            funcs.append(fun)
        elif command.startswith("play "):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play").strip())
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content").strip())
            funcs.append(fun)
        elif command.startswith("google search "):  # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search").strip())
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search").strip())
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system").strip())
            funcs.append(fun)
        else:
            print(f"No Function Found. For ({command})")

    results = await asyncio.gather(*funcs)

    # Execute all tasks concurrently.
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result


async def Automation (commands:list [str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True    
if __name__ == "__main__":
    asyncio.run(Automation(["open whatsapp","open instagram"]))