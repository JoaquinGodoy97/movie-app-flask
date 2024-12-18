

# movie-app-flask

The project is a Movie App built using the Flask framework that takes data from a movie API. Using an MVC architecture, the app will allow you to sign up, log in, and have a set of basic functionalities exploring movies and saving them into a wishlist.

You can check the App using the following link: [Go to the website!](https://movie-app-flask.vercel.app/)

The project is also managed in a way that I can track the updates that were made not only through Git but also with the use of Trello:

![trello-image-movie-app](https://dl.dropboxusercontent.com/scl/fi/ncmicrk7xjx6kk7q6w8nf/trello-api-movies-preview.png?rlkey=xxsitax54kiyikn68ajpny0z9&st=zave2pu9&dl=1)

To **test** the app you can use the following *user* -otherwise, you can sign up with a new user:

    {
       "user": "admin",
       "password": "ADMIN"
    }

Keep in mind that by login with an **Admin Account** you can access and try these admin features:

 - [x] **Delete** a user
 - [x] **Assign** admin rights
 - [x] **Change** User Plans (*Free, Premium , Premium+*)

![admin panel features](https://dl.dropboxusercontent.com/scl/fi/yu35kmmaa4wztsdjcuzel/admin-panel-view.png?rlkey=imn2w0zbtuhy0upxttw9e4bd6&st=bilt26nf&dl=1)

> *It is important to consider that when the database is initialized you can assign a SUPER_ADMIN_USERNAME and SUPER_ADMIN_PASSWORD of your preference as an initial value. In this case they are set to default ["admin", "ADMIN"].*

## Purpose

The movie App provides a user-friendly platform for cinema lovers to explore and save a list of movies.
The main idea is to keep track of your all-time discoveries.

## Responsabilities

1. **User management**:
   - Handle user registration and authentication:

      - A pretty basic sign-up with a username and password.
      - Sign-up includes password reminder
      - Validation checks for username and password length.
      - Allows for admin functionality such as deleting a user, assigning admin rights and changing user plans.

2. **Movie search**:
   - Allow to search movies by name.
      - The Homepage works as the website's search engine.
      - Results are fetched from the movie API.

3. **Movies visualization**:
   - Show basic details such as overview, poster picture, and title.
      - Show a determined number of movies per page.
      - Navigation controls for browsing through pages.
      - Alert system for navigation, like when reaching the first or last page.
   
4. **Save/unsave movies**: 
   - Manage a list of movies.
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

_Updates statuses to movies already on the wishlist for visual references - like knowing which of them are already on the wishlist ._

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
      ...
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

---
### GET: /admin-action/user-list
*Fetches a list of all users in the database (users table) already instantiated and ready to be used.*

Request
Response - 200 OK
Body - JSON ex.:
```bash
{
   "users_list": {
		"id":  "int",
		"username":  "str",
		"email":  "str",
		"password":  "str",
		"adminStatus":  "int", // [0, 1] from database
		"user_plan":  "int" // [1,2,3] Depending on the user plan
		}, 
   "message": "success" (ex.)
}
```
Response - 400: Unable to fetch

---
### POST: /admin-action/delete-user/{int : user_id}
*Deletes a user from the database through the admin panel.*

Request
Headers - Bearer token
Body - JSON: No body

Response - 200 OK :
```bash
{
   "message": "User deleted."
}
```
Response - 206 :
```bash
{
   "message": "User has movies in its account. Want to proceed?"
}
```
Response - 401 : Could not find user
Response - 440 : SESSION_EXPIRED or UNAUTHORIZED

---
### POST: /admin-action/update-admin-rights/ {int : user_id}
*Updates admin rights(boolean) to a user from the database through the admin panel.*

Request
Headers - Bearer token
Body - JSON: No body

Response - 200 OK : User updated.

Response - 400 : Could not update admin rights.

Response - 401 :
```bash
{
   "message": "Cannot update admin status of SUPER ADMIN."
}
```
Response - 440 : SESSION_EXPIRED or UNAUTHORIZED

---
### GET: /admin-action/change-plan/ {int : user_id} /  {int : new_plan} 
*Updates user's plan (1 - free, 2 - premium,3 - premium+) to any of the chosen plans.*

Request
Headers - Bearer token
Body - JSON: No body

Response - 200 OK : User plan updated.
Response - 400 : Failed to update.

--------------------------------------------

## Techs

• Flask
• Python
• Sqlite
• React
• Jwt
• Docker
• MySql
