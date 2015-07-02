Yosemite Scraper
================

Notifies you when campsites near yosemite become available.

Usage
-----

```bash
cp example.secrets.py secrets.py    # Make a real secrets.py file
vim secrets.py                      # Fill in the mailgun secrets
virtualenv --no-site-packages .     # Create a virtualenv
source bin/activate                 # Enter it
pip install -r requirements.txt     # Install python dependencies 
python scraper.py                   # Run the scraper
```
