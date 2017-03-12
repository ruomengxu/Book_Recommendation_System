# recommendation
Book Recommendation System 
1) Data Preperation

Folder contains all scripts that went into the accumulation, cleaning, processing, reduction, feature extraction and assembly of the final dataset. This folder is not necessary to run the final recommender app, but represents the bulk majority of our work.

2) MongoDB

Is the ready to go database for the app. With default port(27017) settings on localhost, run:
mongod --dbpath path-to-Class-Package-folder\MongoDB

3) Eve

Eve is the REST interface for the database. After running MongoDB simply go to the Eve folder and run:
pip install git+https://github.com/nicolaiarocci/eve.git@develop
python run.py

4) Client

This is the client/web page for the app. Simply serve it on a local server. I use brackets.io. The current client cannot handle inputs that deviate from the exact titles in the database. We setup an external autocomplete service to mitigate this but it is working sporadically and mostly not at all. We have included a titles.json file in the client folder that contains all the titles in the database. Find some examples for convenience below:

Failure (No features could be extracted for these titles.):
The Biggest Game
The Learning Maze

Success (All features were extracted and matched to other books successfully.):
Abyss
The Man Who Lived Twice

Partial Success (Some features were extracted and whatever available was used for a partial match.)
The Lord of the Rings
