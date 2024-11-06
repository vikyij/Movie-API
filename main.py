from fastapi import FastAPI, HTTPException
import uvicorn
import json

app = FastAPI()

def load_movies(): 
     with open('data.json', 'r') as file:
        return json.load(file)

@app.get('/getmovies')
def getmovies():
    movies = load_movies()
    return movies

@app.get('/getmoviesbyyear/{year}')
def getmoviesbyyear(year: int):
    movies = load_movies()
    movie_year = []
    for movie in movies:
        if int(movie['releaseYear']) == year:
            movie_year.append(movie)
    if movie_year:
         return movie_year
    else:
        raise HTTPException(status_code=404, detail="No movies found for the specified year.")

@app.get('/getmoviesummary/{movie_title}')
def getmoviesummary(movie_title: str):
    movie_title = movie_title.replace('_', ' ')
    movies = load_movies()
    for movie in movies:
        if movie['title'].lower() == movie_title.lower():
            movie['generatedSummary'] = 'A mind-bending sci-fi thriller about dream theft and manipulation.'
            return movie
    raise HTTPException(status_code=404, detail="Movie not found.")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
