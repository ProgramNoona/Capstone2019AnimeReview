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


admin login
-----------
Username: admin@anirater.com
Password: apple


******************************
Special notes on program tools
******************************
(1.) importcsv.py - This tool is the backbone for populating the database and is used to recreate the database using the anime.csv file. It is continually updated as the file models.py changes. It also currently creates the single admin user (admin@anirater.com). Simply run the file in its current location if you need to recreate site.db and when prompted type anime.csv and hit enter. The bottom function def imagedownloader() can be used to download images from google using specific arguments.

(2.) crud.py - This program is now outdated and doesn't fit the current User table model. It's currently left in for referencing purposes.