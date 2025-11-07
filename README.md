# Project Name 


### Goal:

Goal 


### Requirements: 

- Python 3.13


### Running:

##### Windows:

```
git clone https://github.com/nhimsel/project-csc3070
cd project-csc3070
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd Project
python main.py
```

##### Linux:  

Linux builds are currently functional, though support will be broken 
for future functionality if needed

```
git clone https://github.com/nhimsel/project-csc3070
cd project-csc3070
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd Project
python main.py
```

### Configuration:

Configuration is done in `config.json`
This file should be located in the same directory as `main.py`


##### Options

```
api_url - url for openai-compatible llm api (default: http://127.0.0.1:5000/v1/chat/completions)
```
