# silent-night
##### A new take on werewolf, with full online capabilities
No need to sign in, or create an account. Simply open the page, create or join a lobby and play. Only requirement is to create a temporary username

## Backend
Using flask for simplicity. 
Will be using Redis to maintain memory for game codes and lobby information
Code is separated into 3 python files.
game.py is for most of the logic and the classes.
app.py is for Flask and handling websockets
redis_service is connecting information from lobby to redis and to app.py

## Frontend
Vue
Currently have a template that has nothing to do with the app
Setup to use TypeScript if preferred.
