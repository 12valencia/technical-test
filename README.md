This application allows you to get information about a movie, such as its title, genres, and release date, along with weather data (min and max temperatures) in Madrid on the movie's release date. It uses the TMDB API to get movie data and the Open-Meteo API to fetch weather data.

Install the required dependencies:
1. pip install flask requests
2. run the app.py file:


When you run the application, it will ask you to enter the movie title. It will then display the movie information, including:

Title
Genres
Release Date
If the movie was released after 2016, the app will attempt to fetch weather data for the max and min temperatures in Madrid on that date. If weather data is not available, it will indicate that the data could not be retrieved.

Methodology for movies released before 2016: If the movie was released before 2016, the application will use data from Open-Meteo, which may not provide temperatures. In that case, a message will show that no data was found.