***
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
README.TXT
***

To get started, you will need to install the libraries below. I would suggest using anaconda prompt as it makes the process simple.
This project follows the flask tutorials found at "https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH".

Run the commands below in anaconda prompt:

pip install flask-bcrypt
pip install flask-login
pip install flask
pip install flask-wtf
pip install flask-SQLAlchemy
pip install sqlalchemy
pip install Pillow
pip install sqlalchemy-media

After you have installed the libraries, navigate to the directory containing the program "run.py" in anaconda prompt:

cd <path>  ( path being the directory path where the folder was saved )

Once there, enter the command: 

python run.py

This command will enable flask and sqlalchemy to run on the localhost.

once running, open your browser and navigate to the following address:

http://127.0.0.1:5000

***** other notes *****
importcsv.py allows you to specify the csv file (currently anime.csv) to import its variables to the database. Used mainly for first initializing the database and testing purposes. The old database file should be deleted before doing so.

http://127.0.0.1:5000/anime allows you to input anime through a form but is only accessable through the admin username
email: admin@anirater.com password: apple
