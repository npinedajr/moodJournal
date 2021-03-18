# moodJournal

## Description
  This REST API allows a user to create an account and log in to store string values into a database. These string values are attached to a record known as Mood, which also contains the date the value was stored, the username of the user who created the record, and the streak rating currently being held. The streak rating increases with each consecutive day that a user stored a Mood record and resets to 1 when the streak is broken. Users can also see all Mood records created by their username that are currently stored in the database.
  
## API Guide

**A software application that functions as an API Client, such as Postman, is needed to test the functionality of the REST API.** 

When application.py is downloaded and stored in a directory, the user must create a virtual environment within the directory. To do this, a user should enter the following into their terminal emulator:

```
py -m venv .venv
```

Please note that the python command may be different depending on your current version of Python installed. To enter the virtual environment, you must enter one of the two following lines into the terminal emulator which may differ based on your OS:

```
source .venv/Scripts/activate
source .venv/bin/activate
.venv\Scripts\activate
```

If using a Mac, please use the second line. The first and third line may be used depending on the software installed. Now in the virtual environment, use pip to install flask, flask-login, and flask-SQLAlchemy. Once finished downloading these three packages, it is important to install SQLAlchemy version 1.3.23 to ensure the program works properly. Next, the user must create their database by running the command that will open python in their virtual terminal:

```
py 
python3 
```

The database for the API will be created here. To do so, run the following lines: 

```
from application import db
db.create_all()
```

Now that the database is created, enter exit() into the terminal. It is time to start running the REST API! Enter the following (export may be swapped for set depending on OS):

```
export FLASK_APP=application.py 
export FLASK_ENV=development
flask run
```

Copy the URL provided by the terminal and paste it into Postman and similar software to utilize the API! To save Mood records, a user must first create a new User record with the /user end point and the POST method. The username and password can be set as a key-value pair in JSON style in the Body tab of Postman:
		                                                 { “username”: “<username here>” , “password” : “<password here>”}
In Postman, there should be an Authorization tab in the workspace that holds the URL to the API. This tab is used to login. Basic Authorization is used. Once a user is created, Mood records may now be obtained or created once logged in through the /login endpoint. The description for a mood record may be inserted through the Body tab in the Postman workspace in the typical JSON style, where the key is “description” and the value is a string.

## Product Application Changes
As a product application, instead of simply returning text at the end of each function, the API would return templates to make it easier for users to interact with the API through online forms, instead of having to rely on an external application like Postman. 

Currently, the API does not offer much security with how the passwords are currently treated. For example, someone can just set their password as a single digit. I would improve security by requiring a user to enter a minimum amount of characters, with other requirements such as at least one number, one letter, and one special character,. It also may be worth considering creating an email column for the User records so that in case a user forgets their password, they still have a way to retrieve their account. 

The API currently uses Flask’s built-in server, which will store all data locally. Using the built-in server will be problematic when there are several user records and mood records, so it would be better to deploy the API with a WSGI server instead.
