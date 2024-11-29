
# movie-app-flask

The project is a Movie App built using Flask framwork that takes data from a movie API. Using an MVC architecture, the app will allow you to Sig-up, Log-in and have a set of basic functionalities exploring movies and save them into a wishlist.

You can check the App on the following link: [Go to the website!](https://movie-app-flask.vercel.app/)

To test the app you can use the following user -otherwise you can sign up with a new user:
{
   "user": "admin",
   "password": "ADMIN"
}

## Purpose

The movie App runs to provide a user-friendly platform for cinema lovers to explore and save list of movies.
The main idea is to keep track of your all-time discoveries.

## Responsabilidades

1. **User management**:
   - Handle user registration and authentication:

      - A pretty basic sign-up with username and password.
      - Sign-up includes password reminder
      - Validation checks for username and password length.

2. **Movie search**:
   - Allow to search movies by name.
      - Homepage landing page working as search engine of the website.
      - Results are fetched from the movie API.

3. **Movies visualization**:
   - Show basic details as overview, poster picture and title.
      - Show determined number of movies per page.
      - Navigation controls for browsing through pages.
      - Alert system for navigation, like when reaching the first or last page.
   
4. **Save/unsave movies**: 
   - Manage list of movies.
      - Add or remove movies from a personalized wishlist.
      - Add/delete button functionality for individual display.
      - Communication between movie results service and Wishlist service.

**Setup Instructions**

To run the app locally using Docker, follow these steps:

1. **Build and Start the Containers**:
   ```bash
   docker-compose build
   docker-compose up -d

## API DOCUMENTATION

### POST: /login

_Authenticates the user and issues a JWT token if credentials are valid._

Request
Body - JSON ex.: 

    {
       "username": "string",
       "password": "string"
    }

Response - 200 OK
Headers - TOKEN
Redirect - /search
Body - JSON ex.:
```bash
   {
      "message": MSG_WELCOME_MSG or MSG_NEW_USER_CREATED,
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }
```
Response - 401 : Unauthorized: INVALID CREDENTIALS. 
Redirect - /login.

Response - 440 : SESSION_EXPIRED or UNAUTHORIZED
Redirects - /login.

---
### POST: /logout
 
_Logs the user out by invalidating their session._

Response - 200 OK
Redirect - /login

---
### GET: /@me

_Retrieves details of the currently authenticated user._

Hearders - Authorization TOKEN

Response - 200 OK
Redirect - /search

Response - 401 : Unauthorized: INVALID CREDENTIALS. 
Redirect - /login

Response - 440 : SESSION_EXPIRED or UNAUTHORIZED
Redirect - /login

---
### GET: /results/search

_Searches and retrieves movie results._

Response - 200 OK
Body - JSON ex.:
```bash
{
   "results": "dict", // By sets of 5 movies
   "total_pages": "int",
   "redirect": "/results"
}
```

Response - 404 : Page not found.

Response - 440 : SESSION_EXPIRED or UNAUTHORIZED
Redirect - /login

---
### GET: /wishlist

_Fetches the user's wishlist._

Response - 200 OK
Body - JSON ex.:
```bash
{
   "results": "dict", - By sets of 5 movies in DB
   "total_pages": "int",
   "redirect": "/wishlist"
}
```
Response - 404 : Page not found.

Response - 440 : SESSION_EXPIRED or UNAUTHORIZED
Redirect - /login

---
### POST: /wishlist/add/{movie_id}/{movie_name}

_Adds a movie to the user's wishlist._

Request 
Headers - Bearer token
PathParam - {movie_id: int, movie_name: str}

Response - 200 OK 
Body - JSON: 
```bash
{
   "message": "Movie added."
   "method": "add"
}
```
Response - 400 : Bad movie request - Invalid movie_id or movie_name

Response - 409 : Movie already added.

Response - 403 : Movies limit reached. - Max. 50 per user

---
### POST: /wishlist/remove/{movie_id}

_Removes a movie to the user's wishlist._

Request
Headers - Bearer token
PathParam - {movie_id: int}

Response - 200 OK 
Body - JSON: 
```bash
{
   "message": "Movie removed."
   "method": "remove"
}
```
Response - 400 : Bad movie request. - Invalid movie_id

Response - 409 : Movie already added.

Response - 403 : Movies limit reached. - Max. 50 per user

---
### GET: /wishlist/search

_Searches and retrieves movie results inside wishlist's user page._

Response - 200 OK
Body - JSON ex.:
```bash
{
   "results": "dict", // By sets of 5 movies
   "total_pages": "int",
   "redirect": "/wishlist"
}
```
Response - 404 : Page not found.

Response - 440 : SESSION_EXPIRED or UNAUTHORIZED
Redirect - /login

---
### POST: /wishlist-status

_Updates movies statuses to those movies which are already on the wishlist for visual purposes._

Request
Headers - Bearer token
Body - JSON: No body

Response - 200 OK 
Body - JSON: 
```bash
{
   "statuses": {
      "movie_id": "boolean",
      "movie_id": "boolean"
   }
}
```
Example
```bash
{
   "statuses": {
      "101": true,
      "102": false
   }
}
```
Response - 440 : SESSION_EXPIRED or UNAUTHORIZED

--------------------------------------------

## Techs

• Flask
• Python
• Sqlite
• React
• Jwt
• Docker
