# CSV Atlas
Upload, display, and download CSV files to your heart's content. 
If your csv has a 'state' column, missing entries will be displayed with BLANK.
If any columns in your csv can be typecast as pandas datetime datatypes, the "Stats" button will display counts
for all entries in the row with the same year value.

## GETTING STARTED

These instructions will get you a copy of the project up and running locally.
Dependencies are python3 and pip.

### Clone repository to desired location
```
git clone https://github.com/jakemobley/csv_atlas.git
```

### Setup virtual environment

Lately for basic projects I have been using pipenv since it doesn't require naming or frequent sourcing, but venv is 
sometimes easier.
```
python -m venv whatever_env
```
Don't forget to activate.

From there you can check out this resource for some common setup items: 
https://docs.python-guide.org/dev/virtualenvs/ or just use whatever virtual environment you want.

### Install requirements
```
pip install -r requirements.txt
```

### Initialize Flask development server if you want; may need 'python3' depending on your interpreter
```
python main.py
```

With your development server open you can now visit the landing page in your local browser.
```
localhost:5000/
```

## CUSTOMIZE / ADDITIONAL

Make sure to visit config.py and select which folders you would like to use to store your files.

Change/add routes and templates and customize to your heart's unbridled content. My main.css file is located in /static and is linked to layout.html.

Deployment should be fairly easy using the services of your choice. I tested deployments using App Engine on 
Google Cloud Platform and linux servers using nginx and gunicorn.

## FAQ / CONTACT / TROUBLESHOOT

Contact me with questions at jakemobley[at]gmail[dot]com and I will answer as best I can.

## ACKNOWLEDGEMENTS

This project is licensed under the GNU License - see the LICENSE.md file for details.
