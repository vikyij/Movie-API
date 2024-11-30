from fastapi import FastAPI, HTTPException
import uvicorn
import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI()


# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get table
table = dynamodb.Table('Movie-data')


app = FastAPI()

@app.get('/getmovies')
def getmovies():
    # Get all movies from Dynamodb
    try:
        response = table.scan()
        items = response["Items"]
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getmoviesbyyear/{year}')
def getmoviesbyyear(year: str):
    # Get movies by year
    try:
        response = table.query(
        IndexName= "releaseYearIndex",
        KeyConditionExpression=Key('releaseYear').eq(year)
        )
        movies = response["Items"]
        if movies:
            return movies
        else:
            raise HTTPException(status_code=404, detail=f"No movies found for the specified year {year}.")
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/getmoviesummary/{movie_title}')
def getmoviesummary(movie_title: str):
    movie_title = movie_title.replace('_', ' ')
    # STEP 1: Get Items by Title
    try:
        response = table.scan(
            FilterExpression=Attr('title').eq(movie_title.lower())
        )
        movies = response["Items"]
        if not movies:
            raise HTTPException(status_code=404, detail='Movie not found')
        movie=movies[0]
       
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # STEP 2: Generate the AI Summary
    try: 
        prompt = (f"Write a brief and engaging summary for the movie '{movie['title']}' "
            f"which was released in {movie['releaseYear']} and belongs to the genre {movie['genre']}.")
 
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
        return(completion.choices[0].message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating AI summary: {str(e)}")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
