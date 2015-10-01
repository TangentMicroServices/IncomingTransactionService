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

The Simplest Request Sequence for a successful Hours Entry

```
{ "user": "4",
  "project_id": "3",
  "project_task_id" : "5",
  "time": "{{OccurredAt}}"
  "entered_or_exited": "entered"}
```

Followed by:

```
{ "user": "4",
  "project_id": "3",
  "project_task_id: "5",
  "time": "{{OccurredAt}}".
  "entered_or_exited": "exited"}
```

With the following conditions:
* `entered` and `exited` must occur within 24 hours of each other

#### Setting up the Maker Request for Automatic Hours Logging with Location

1. Go to [IfThisThenThat](https://ifttt.com) Website
or download the [iOS](https://itunes.apple.com/za/app/if-by-ifttt/id660944635?mt=8) or [android](https://play.google.com/store/apps/details?id=com.ifttt.ifttt&hl=en) apps.

2. Go to `My Recipes` -> `Create a Recipe`

3. Click on `this` then add `Android` or `iOS` location

4. Choose the trigger `You enter or Exit an Area`

5. Choose the Area

6. Create Trigger

7. Click on `that` then add `Maker`

8. `Make a Web Request`

9. Use the follwing data

    ```
    url : TBA
    method: post
    content-type: application/json
    body:
    { "user": "<<your_id_here>>",
      "project_id": "<<project_id_here>>",
      "project_task_id: "<<project_task_id here>>",
      "time": "{{OccurredAt}}".
      "entered_or_exited": "{{EnteredOrExited}} "}
    ```

10. Create the Action, give it a relevant name. Eg. `african_bank_hours_area`

11. `Create`
