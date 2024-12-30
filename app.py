import requests
from datetime import datetime

# TMDB API Key (replace with your own key)
TMDB_API_KEY = "ed011a6a8854357fa5fe1f7029b9d19e"

# URL for Open-Meteo API (use to get the weather data)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Function to get movie data from TMDB
def get_movie_data(movie_title):
    """Fetches movie data from TMDB."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie = data["results"][0]  # Take the first movie found
            
            # Get genre names
            genre_ids = movie.get("genre_ids", [])
            genres = get_genre_names(genre_ids)
            
            return {
                "title": movie["title"],
                "genres": genres,
                "release_date": movie["release_date"],
            }
    return None

# Function to get genre names from genre IDs
def get_genre_names(genre_ids):
    """Fetches genre names based on their IDs."""
    genre_names = []
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(genre_url)
    if response.status_code == 200:
        data = response.json()
        genre_map = {genre["id"]: genre["name"] for genre in data["genres"]}
        
        # Map genre IDs to names
        for genre_id in genre_ids:
            if genre_id in genre_map:
                genre_names.append(genre_map[genre_id])
    return genre_names

# Function to get weather data from Open-Meteo
def get_weather_data(movie_release_date, city="Madrid"):
    """Fetches weather data for a city on a specific date."""
    try:
        # Convert release date to datetime format
        release_date = datetime.strptime(movie_release_date, "%Y-%m-%d")
    except ValueError:
        print("Error processing release date")
        return None

    year, month, day = release_date.year, release_date.month, release_date.day

    # City coordinates (Madrid in this case)
    city_coordinates = {
        "Madrid": {"latitude": 40.4168, "longitude": -3.7038},
        # You can add other cities here if needed
    }

    # Get city coordinates
    city_data = city_coordinates.get(city)
    if not city_data:
        print(f"City {city} not found.")
        return None

    latitude = city_data["latitude"]
    longitude = city_data["longitude"]

    # Build URL for Open-Meteo API
    weather_url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&start_date={year}-{month:02d}-{day:02d}&end_date={year}-{month:02d}-{day:02d}&timezone=Europe/Madrid"
    
    response = requests.get(weather_url)
    
    # Check response from Open-Meteo API
    if response.status_code == 200:
        try:
            data = response.json()
            # Ensure 'daily' key exists and has data
            if "daily" in data and isinstance(data["daily"], list) and len(data["daily"]) > 0:
                daily_data = data["daily"][0]  # First entry of the day
                return {
                    "min_temp": daily_data.get("temperature_2m_min", "No data"),
                    "max_temp": daily_data.get("temperature_2m_max", "No data")
                }
            else:
                print("No daily data found for the provided date.")
        except ValueError:
            print("Error processing weather API response.")
    else:
        print(f"Error in weather query: {response.status_code} - {response.text}")
    return None

# Main function
def main():
    movie_title = input("Enter the movie title: ")

    # Get movie data
    movie_data = get_movie_data(movie_title)
    if movie_data:
        print(f"\nMovie Information: ")
        print(f"Title: {movie_data['title']}")
        print(f"Genres: {', '.join(movie_data['genres'])}")
        print(f"Release Date: {movie_data['release_date']}")

        # Get weather data for release date (or current date if needed)
        weather_data = get_weather_data(movie_data["release_date"])
        if weather_data:
            print(f"\nWeather Information:")
            print(f"Min Temperature on release date: {weather_data['min_temp']}°C")
            print(f"Max Temperature on release date: {weather_data['max_temp']}°C")
        
            # Send data to a webhook
            data = {
                "movie": movie_data,
                "weather": weather_data
            }
            webhook_url = "https://eo9m0nh4z7lacho.m.pipedream.net"
            requests.post(webhook_url, json=data)
            print("\nData sent to the webhook.")
        else:
            print("\nCould not retrieve weather data.")
    else:
        print("\nMovie not found.")

# Run the program
if __name__ == "__main__":
    main()
