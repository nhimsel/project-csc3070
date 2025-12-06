# Project Name 


### Goal:

Goal 


### Requirements: 

- Python 3.13
- `requirements.txt`

Creating a venv is recommended if not using a pre-compiled binary. 

To create and install dependencies in a venv, run the following in the project root:
```
python -m venv venv
venv\scripts\activate.bat
pip install -r requirements.txt
```

Once the venv is created, it can be activated with `venv\scripts\activate.bat`.

### Compilation:

From the project's root, run `make`.

### Running:

From the `Project` directory, run `python main.py`.

### Configuration:

Configuration is done in `config.json`.

If compiled to an exe, `config.json` should be in the same directory as the exe.

If not compiled, `config.json` should be in the same directory as `main.py`.

#### Options

- `api_url` - url for openai-compatible llm api (default: http://127.0.0.1:5000/v1/chat/completions)
- `hide_on_fullscreen` - can be true or false. determines whether the buddy is visible when a fullscreen app is detected