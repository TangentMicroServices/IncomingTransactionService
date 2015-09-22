# IncomingTransactionService

A service for fielding incoming webhooks

## Local setup:

1. Clone the repo
2. We'll use python3 for this project: 

        virtualenv-3.4 ~/Projects/venvs/webhooks -p python3
        
3. Activate your env:
 
        source env/bin/activate
        
4. Verify you've got the correct version of python:

        python --version
        
5. Install requirements

        pip install -r requirements.txt
        
5. Setup db

		python manage.py migrate
        
5. Run a local server:

        python manage.py runserver
        
6. Run tests:

        python manage.py test
        
7. Profit

## Webhook handlers

### Webhook

This is the base handler. It provides a basic model for saving an incoming request as well as base reusable functionality

### Hipchat

Catch [incoming `/slash` commands from Hipchat](https://blog.hipchat.com/2015/02/11/build-your-own-integration-with-hipchat/)

### Mandrill

Handling incoming email from Mandrill 

### IFTTT

Handle incoming webhooks from the [maker plugin for IFTTT](https://ifttt.com/maker)

...
        
