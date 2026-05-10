from fastapi import FastAPI
from parser import load_subtitles, create_scene_chunks
from retrieval import create_index, search

app = FastAPI()

all_chunks = []


@app.get("/")
def home():
    return {
        "message": "CineMind API Running"
    }


@app.get("/load")
def load_data():

    global all_chunks

    files = [
        ("The Dark Knight", "data/dark_knight.srt"),
        ("Interstellar", "data/Interstellar.srt"),
        ("The Devil Wears Prada", "data/Devil_Wears_Prada_2.srt")
    ]

    combined_chunks = []

    for movie_name, path in files:

        scenes = load_subtitles(path)

        for scene in scenes:
            scene["movie"] = movie_name

        chunks = create_scene_chunks(scenes)

        combined_chunks.extend(chunks)

    create_index(combined_chunks)

    all_chunks = combined_chunks

    return {
        "chunks_loaded": len(combined_chunks)
    }


@app.get("/search")
def search_scenes(query: str):

    results = search(query)

    return {
        "query": query,
        "results": results
    }