# movie-app-flask

<!-- #first step idea    
This is a movie App that takes data from a movie API. In general, I am using flask framework for the backend coding. For displaying I used Bootstrap and a bit of CSS. The app also includes  a custom pagination functionality as well as a basic display of a list of movies. -->

The project is a Movie App built using Flask framwork that takes data from a movie API. Using an MVC architecture, the app will allow you to Sig-up, Log-in and have a set of basic functionalities exploring movies and save them into a wishlist.

You can check the App on the following link: https://movie-app-flask.onrender.com/search

## Purpose

The movie Aoo auns to provide a user-friendly platform for cinema lovers to explore and save list of movies.
The main idea is to keep track of your all-time discoveries.

## Responsabilidades

1. **User management**:
   - Handle user registration and authentication:

      • A pretty basic sign-up with username and password.
      • Sign-up includes password reminder
      • Validation checks for username and password length.

2. **Movie search**:
   - Allow to search movies by name.
      • Homepage landing page working as search engine of the website.
      • Results are fetched from the movie API.

3. **Movies visualization**:
   - Show basic details as overview, poster picture and title.
      • Show determined number of movies per page.
      • Navigation controls for browsing through pages.
      • Alert system for navigation, like when reaching the first or last page.
   
4. **Save/unsave movies**: 
   - Manage list of movies.
      • Add or remove movies from a personalized wishlist.
      • Add/delete button functionality for individual display.
      • Communication between movie results service and Wishlist service.

**Setup Instructions**

Run dockerfile with the following settings:
------------------------------------------

FROM python:3.12.4

WORKDIR /api-movies

COPY requirements.txt .
COPY . /api-movies

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

--------------------------------------------

You can also download the requirements in requirements.txt:

pip install -r requirements.txt

**Technologies Used**

Flask: Python web framework used for developing the web application.
HTML/CSS: Frontend technologies used for structuring and styling the web pages.
SQLite: Database used for storing user data and movie information.
Themoviedb.org API: External API used to fetch movie data.
Bootstrap: CSS framework used to design responsive and mobile-first web pages.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    proposito
    responsabilidades (funciones ex. lsitar pelis de api tal)
    -api documentation (ex. swagger, coleccion de postman para probar app)
    -como levantar la app (pasos de como levantarla)
    -tecnologias
    -intro

    