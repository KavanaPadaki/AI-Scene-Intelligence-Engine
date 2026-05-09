from fastapi import FastAPI
from parser import load_subtitles, create_scene_chunks
from retrieval import create_index, search

app = FastAPI()

all_chunks = []


@app.get("/")
def home():
    return {
        "message": "CineMind API running"
    }


@app.get("/load")
def load_data():
    global all_chunks

    scenes = load_subtitles("data/dark_knight.srt")

    chunks = create_scene_chunks(scenes)

    create_index(chunks)

    all_chunks = chunks

    return {
        "chunks_loaded": len(chunks)
    }


@app.get("/search")
def search_scenes(query: str):
    results = search(query)

    return {
        "query": query,
        "results": results
    }