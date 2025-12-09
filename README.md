# Project Name 


### Goal:

Goal 

### Downloads

Downloads for pre-built binaries can be found under [Releases](https://github.com/nhimsel/project-csc3070/releases).


### Configuration:

The configuration is best done via the `Settings` panel found in the tray icon. 

If using a compiled exe, the config file will be in the `_internal` directory.

If directly running via python, the config file will be in the same directory as `main.py`.

#### Options

- `api_url` - url for openai-compatible llm api (default: http://127.0.0.1:5000/v1/chat/completions)
- `hide_on_fullscreen` - can be true or false. determines whether the buddy is visible when a fullscreen app is detected (default: False)
- `outfit` - folder in `anims` directory that contains the buddy's active appearance. (default: `default`)


### Development Requirements: 

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
If you created a venv, ensure it is activated.

Note that `make` is not explicitly required for compiliation.
For compiliation without `make`, see the `Makefile` for direct commands.

### Running Without Compiliation:

From the `Project` directory, run `python main.py`.
