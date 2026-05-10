import pysrt
import re


def load_subtitles(file_path):
    """
    Load subtitle file and return parsed subtitle entries.
    """

    subs = pysrt.open(file_path)

    scenes = []

    for sub in subs:

        cleaned_text = (
            sub.text
            .replace("\n", " ")
            .replace("`", "")
            .replace("-", "")
            .strip()
        )

        # Remove HTML tags like <i>...</i>
        cleaned_text = re.sub(r"<.*?>", "", cleaned_text)

        # Skip empty subtitles
        if not cleaned_text:
            continue

        scene = {
            "start": str(sub.start),
            "end": str(sub.end),
            "text": cleaned_text
        }

        scenes.append(scene)

    return scenes


def create_scene_chunks(scenes, chunk_size=10):
    """
    Group subtitle entries into larger contextual chunks.
    """

    chunks = []

    for i in range(0, len(scenes), chunk_size):

        group = scenes[i:i + chunk_size]

        if not group:
            continue

        combined_text = " ".join(
            [scene["text"] for scene in group]
        )

        chunk = {
            "movie": group[0]["movie"],
            "start": group[0]["start"],
            "end": group[-1]["end"],
            "text": combined_text
        }

        chunks.append(chunk)

    return chunks


# Local test
if __name__ == "__main__":

    file_path = "data/dark_knight.srt"

    scenes = load_subtitles(file_path)

    print(f"Loaded {len(scenes)} subtitle entries")

    # Add movie name manually for local test
    for scene in scenes:
        scene["movie"] = "The Dark Knight"

    chunks = create_scene_chunks(scenes)

    print(f"Created {len(chunks)} chunks")

    print("\nSample Chunk:\n")

    print(chunks[0])