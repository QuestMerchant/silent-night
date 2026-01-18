# silent-night
##### A new take on werewolf, with full online capabilities
No need to sign in, or create an account. Simply open the page, create or join a lobby and play. Only requirement is to create a temporary username

## Backend
Using flask for simplicity. 
Will be using Redis to maintain memory for game codes and lobby information
As the free tier of Python Anywhere doesn't support websockets, this app will be making use of Pusher instead of socketIO.
Code is separated into 4 python files.
game.py is for most of the logic and the classes.
app.py is for Flask and handling websockets
redis_service.py is connecting information from lobby to Redis and to app.py
voting.py as a module for voting functions
Must change the time module to asyncio and use async functions for the timer to avoid blocking casting votes while the timer runs.

## Frontend
Vue
Using Quasar framework for CSS & JS


#### Choices
Use jsonify after http request for specific user, otherwise use Pusher to send information for all users.
In instances such as joining a lobby, both should be used. Send a HTTP request POST, jsonify the lobby to the user, and emit via socket, within the Flask @app.route function, to all users that this user has joined.
Sockets can be sent to the chat section (excluding votes). create a profile for server messages (user join, someone eliminated etc.).

###### Cookies (frontend functionality to save resources)
Due to being unable to send arguments when pushing to a new vue route, set the user_id as a cookie. Then recall the cookie after redirect to restore user_id.
Functions for setting and getting cookie are in util. 
import { fetchCookie, setCookie } from '@/util/cookies'
To set a cookie, simply use setCookie(name, value, expiry). Where name is the name of the cookie as a string, value is the value of the variable to be stored, expiry is number of days to keep cookie. AKA, cookie1 = setCookie("user_id", '1234', 60). This will store 'user_id':'1234' for 2 months

