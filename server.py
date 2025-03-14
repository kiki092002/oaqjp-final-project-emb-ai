
from flask import Flask, render_template, request
import requests
from EmotionDetection.emotion_detection import emotion_detector
app = Flask(__name__)



# Function to map emotion to a movie title
def map_emotion_to_movie(emotion):
    emotion_to_movie = {
        "joy": "Interstellar",  # Cheerful, uplifting
        "sadness": "The Pursuit of Happyness",  # Emotional, touching
        "anger": "Mad Max: Fury Road",  # Intense, action-packed
        "fear": "A Quiet Place",  # Suspenseful, horror
        "disgust": "The Hangover",  # Comedy
        "surprise": "Inception"  # Mind-bending, thrilling
    }
    return emotion_to_movie.get(emotion, "Interstellar")  # Default movie if emotion not mapped

# Function to fetch movie details from OMDb API based on the movie title
def get_movie_details(movie_title):
    api_key = "d735b6e"  # Replace with your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Route to analyze the emotion of the provided text and recommend a movie
@app.route("/emotionDetector")
def sent_analyzer():
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    
    if text_to_analyze:
        # Pass the text to the emotion_detector function to get the dominant emotion
        dominant_emotion = emotion_detector(text_to_analyze)
        
        if dominant_emotion != "No emotion detected.":
            # Map the dominant emotion to a movie title
            movie_title = map_emotion_to_movie(dominant_emotion)
            
            # Fetch movie details from OMDb API based on the movie title
            movie_details = get_movie_details(movie_title)
            
            if movie_details and movie_details['Response'] == 'True':
                return render_template('result.html', emotion=dominant_emotion, movie=movie_details)
            else:
                return f"Error: Movie details not found for {movie_title}."
        else:
            return dominant_emotion
    else:
        return "Please provide text to analyze."

# Route to render the index page
@app.route("/")
def render_index_page():
    return render_template('index.html')

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
