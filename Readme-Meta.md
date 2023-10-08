# MetaReadme

This repo github-actions-test is a playground for changes we want to make to the mac-mouse-fix repo for the MMF 3 release. Specifically, it deals with user changing updates. Currently it contains a new Readme.md file and a new Acknowledgements.md file as well as a template plus python script to generate Acknowledgements.md. 

This repo also contains experiements on using GitHub Actions. IIRC we planned to use GH Actions to run the Acknowledgements generation script every time a new copy of MMF was purchased. But we found it impossible for a Gumroad purchase to trigger a GitHub action, so we decided to just run the update script periodically.

# Install dependencies into python env

To run the python script which generates Acknowledgements.md, activate `markdown_env` with the command: (In fish shell)

```
source MarkdownStuff/markdown_env/bin/activate.fish
```

And deactivate with 

```
deactivate
```

I just found out that venvs aren't portable at all! but we can create a requirements.txt file which is portable.
In update-acknowledgements.yml we generate a new venv with the requirements for the python script based on the requirements.txt file.

You can freeze the currently activated env into a requrements.txt using

```
pip freeze > MarkdownStuff/python_requirements.txt
```

You can create a new venv and install the python_requirements.txt file like this:

``````
python3 -m venv env;\
source env/bin/activate.fish;\
python3 -m pip install -r Markdown/Code/python_requirements.txt;
``````

# Using markdown_generator.py

To generate the **acknowledgements** document in different languages based on templates
```
python3 Markdown/Code/markdown_generator.py --document acknowledgements --api_key ***
```

If you don't have the api key:
```
python3 Markdown/Code/markdown_generator.py --document acknowledgements --no_api
```

To generate the **readme** document in different languages based on templates
```
python3 Markdown/Code/markdown_generator.py --document readme
```

# Previewing generated markdown files locally

I use VSCode with the plugin: https://marketplace.visualstudio.com/items?itemName=bierner.markdown-preview-github-styles

# Editing a template

1. Install python, create and activate a venv, then install the requirements from Markdown/Code/python_requirements.txt into your venv (see above) (in order to run the markdown_generator.py script)
2. Edit the template under Markdown/Templates/
3. Run the markdown_generator.py script which creates an output file based on the template. To see which templates generate which output files see the 'documents' dictionary at the top of the markdown_generator.py script
4. If the output file looks good, create a pull request

# Add a new template to add a new language for a document

1. Install python, create and activate a venv, then install the requirements from Markdown/Code/python_requirements.txt into your venv (see above) (in order to run the markdown_generator.py script)
2. Create a new template under Markdown/Templates/
3. Add a new entry for your new template to the 'documents' dictionary at the top of the markdown_generator.py script
4. Run the markdown_generator.py script, which creates an output file based on your new template.
5. If the output file looks good, create a commit and a pull request and stuff

# Online GitHub Actions linting

https://rhysd.github.io/actionlint/

# Localization

https://www.techonthenet.com/js/language_tags.php

# Gumroad API

To test the Gumroad sales API (which we use for acknowledgements_generator.py) from the command line:

```
curl --request GET --header "Content-Type: application/x-www-form-urlencoded" --data 'access_token=SECRET&product_id=FP8NisFw09uY8HWTvVMzvg==' https://api.gumroad.com/v2/sales | json_pp
```

# Wrap links in markdown which contain spaces with < and > to make them work

See https://superuser.com/a/1517072/1095998

# GitHub Actions Reference

- Basic concepts: https://dev.to/github/whats-the-difference-between-a-github-action-and-a-workflow-2gba
- Python sript: https://github.com/GuillaumeFalourd/poc-github-actions/blob/main/.github/workflows/03-python-script-workflow.yml
- HTTPs triggers: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch

- HTTP basics: https://www.tutorialspoint.com/http/http_requests.htm
  - Abstraction stack is IP (Packets and routing) -> TCP ('Correct' streams or chunks of data (aka files?)) -> HTTP (Made for webbrowser<->server connection but now also used for other communication)
  - HTTP requests are basically a string of text following a certain format (aka protocol) and then transmitted via TCP.
  - HTTP requests seems to be built around "forms". But all the stuff with "form" in it's name is now also used for other stuff.
    - See: https://eloquentjavascript.net/18_http.html <- This article is great
  - HTTP requests consist of
    - Request line containing METHOD, URI, and HTTP version
      - IIUC the server can map any METHOD to any action. METHODs don't 'do' anything. It's just convention that certain methods trigger certain types of actions.
      - URI specifies "the resource upon which to act". It's bascally the URL without the ?name=value part (aka the Query String). Can also be * for the whole server or a path relative to the server where the request originated. But that's not relevant for us.
    - Optional header(s)
      - These are just random key-value-pairs whose keys are conventionally used and therefore *probably* understood by the receiver
    - Optional body
      - This can be any data in any format. These are the 2 conventionally used formats which can be specified in the header with key "Content-Type":
        - application/x-www-form-urlencoded
          - Data is encoded to look like the queryString (key=value&key2=value2).
          - This is the default and most commonly used.
        - multipart/form-data
          - Body can have several sections all with different headers and encodings. I often read "use this when your form has file uploads"
      - There are also more formats like "application/json", or plaintext. 
      - I think the urlencoded can transmit nested datastructures somehow but not sure.
      - When your url contains a queryString the query string will automatically be made part of the body of the HTTP request (True for POST, not true for GET. Not sure about other METHODS)
        - So do you have to use application/x-www-form-urlencoded when using a queryString?
        - Can you use a queryString and also send additional data? That would probably use `multipart/form-data`.
  - IIUC HTTP is designed for transferring old, static, javascriptless HTML between servers and web browsers. Here, the only method of interaction was forms and links. That's where a lot of the weirdness comes from. Using HTTP Post for general message sending to/from/between servers is also kind of weird, since it has nothing to do with "HyperText" at all. HTTP just became became the standard for all these things it was never designed for. That's why it's so weird.
- TCP (Transfer Control Protocol)
  - Ports seem to be pretty unnecessary. I think ports were originally made to allow for simultaneous connection sessions, but there can be several connection sessions on a single TCP port. Port numbers are conventionally used for specific higher level protocols (e.g. port 80 for HTTP). But I feel like everything would work fine if ports didn't exist.
- UDP (user datagram protocol) is a protocol at around the same level of abstraction as TCP. UDP doesn't do all the correctness checks and is faster. Commonly used for videogames or VoIP.


# Dynamic readmes

- Dynamic readme: 
  - https://github.com/marketplace/actions/dynamic-readme
  - https://github.com/bitflight-devops/github-action-readme-generator
  - https://github.com/marketplace/actions/generate-update-markdown-content
  - https://github.com/marketplace/actions/github-readme-generator
  - > F this I'll just write a simple pythin script that takes a template as format string and then generates this. Maybe run it periodically using github actions
