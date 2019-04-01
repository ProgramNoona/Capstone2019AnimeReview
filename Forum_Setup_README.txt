CSC -289 Capstone project - Forum
Group 3 

*
*	No files are needed to be downloaded for now. This guide is to help set up an 
*	instance of a FlaskBB forum using the framework FlaskBB. 
*	As I complete the primary setup & installations, I will further update
* 	this guide. Only one instance (setup & activation) will be needed. 
*


--- Getting Started & Setup ---


run anaconda prompt as administrator & install the libraries below

*
* MAKE SURE YOU HAVE GIT DOWNLOADED!
* THIS WILL ALLOW YOU TO CLONE FLASKBB
* FROM THE REPOSITORY
*
* https://git-scm.com/downloads		(git download)
*gi

pip install --upgrade pip setuptools

pip install virtualenv 

pip install --user virtualenvwrapper

pip install virtualenv --user


mkdir forum_dir 		(you can call the project whatever you want)

cd forum_dir			(change to project dir)


git clone https://github.com/sh4nks/flaskbb.git

cd flaskbb

git checkout 2.0.0

virtualenv .venv			(you can call it what you want. In this case its .venv)

.venv\Scripts\activate		(activate the virtual environment)
				(If using Linux OS, try:   source .venv/bin/activate)
				(your directory should now be changed)
				(to exit the environment type "deactivate" but not right now)

pip install Flask		(activate flask in the virtualenv)


--- Dependencies ---


pip install -r requirements.txt 

flaskbb makeconfig 		(	if you get an error try this command:
					pip install -r requirements-dev.txt
					
					You will be asked several questions about installation, directory,
					email address, sever name, mail port #, and passwords)

flaskbb --config flaskbb.cfg install	(installation. It is recommended to create a new database for installation)

flaskbb --config flaskbb.cfg run	(	run the the development server.
						visit  "localhost:5000" to test the connection	)

					


