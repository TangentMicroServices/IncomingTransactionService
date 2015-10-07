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

## IFTTT Location Based Automatic Hours

You can do a variety of things with _If This Then That_, the most important for us is: **hours posting based on your entry and exit of a specific area**

### Sequence of Events for Hours Entry

1. Entering an area sends an `entered` request to the `IncomingTransactionService/ifttt`
2. Exiting an area sends an `exited` request to the `IncomingTransactionService/ifttt`
3. Hours are calculated and sent to the `HoursService` with the pay load set in `Ifttt Maker Recipe`

### Setup

1. Go to the [IfThisThenThat](https://ifttt.com) Website
or download the [iOS](https://itunes.apple.com/za/app/if-by-ifttt/id660944635?mt=8) or [android](https://play.google.com/store/apps/details?id=com.ifttt.ifttt&hl=en) apps.

2. Go to `My Recipes` -> `Create a Recipe`

3. Click on `this` then add `Android` or `iOS` location

4. Choose the trigger `You enter or Exit an Area`

    **NB:** Make Sure You Select When `You Enter and Exit an Area`

5. Choose the Area

6. Create Trigger

7. Click on `that` then add `Maker`

8. `Make a Web Request`

9. Use the following data

    ```
    url : http://staging.incoming.tangentmicroservices.com/ifttt/
    method: post
    content-type: application/x-www-form-encoded
    body:
    user=<<UserId>>&project_id=<<ProjectId>>
    &project_task_id=<<ProjectTaskId>>
    &time={{OccurredAt}}
    &entered_or_exited={{EnteredOrExited}}
    &auth_token=<<AuthToken>>&comment=<<Comment>>
    ```
    
    Replace the body above `<<Vars>>` with your corresponding data. They can be found by visiting [hr.tangentme.com](http://hr.tangentme.com/)
    
    An example body might be: 
    
    ```
    user=1&project_id=43&project_task_id=57&time={{OccurredAt}}&entered_or_exited={{EnteredOrExited}}&auth_token= ...&comment=AfricanBank
    ```

10. Create the Action, give it a relevant name. Eg. `african_bank_hours`

11. `Create`

12. Make sure the app is installed on your phone

The maker part of your recipe should look something along the lines of: 

![ifttt recipe](https://s3-us-west-2.amazonaws.com/tangentsolutions.co.za/ifttt.PNG)

### What it Doesn't Do Right Now

* **Changeable Comments** -  If your comments are very specific ie. change with each entry then changing your comment _every time_ in the Maker Request payload is not  worth it. So it is best used if your comments are pretty _generic_

* **Overtime**

* **Multiple Days** - The `day` logged will be the `date` at the time the final `exited` request is received. So if you work past midnight, the hours will be logged for the following day you started work.

* **Hour ranges**: `x < 1 or > 24` - `enter` and `exited` requests must occur within 1 and 24 hours

* **Multiple Project Tasks Same Location**
