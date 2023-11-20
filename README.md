# AzureStreambot

AzureStreambot is a Python Script that gives a tts voice to whomever you want using ws i suggest using streamer.bot[https://streamer.bot]

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **pipenv**.

```bash
pip install pipenv
```
after that use this command to install the dependencies.
```bash
pipenv install --dev
```
this will install the packages specified in the **Pipfile**.
## Usage
first fill the environment file with your data
```env
SPEECH_KEY=''
SPEECH_REGION=''                          
STYLE_DEGREE=                     #no need to fill          
VOICE=''                          #no need to fill                                  
ROLE =''                          #no need to fill            
IP=''                             #no need to fill                                    
PORT=''                           #no need to fill              
```
then run this command in the terminal
```bash
pipenv run python streamazurebot.py
```
you can find out more about these [here](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice) 
