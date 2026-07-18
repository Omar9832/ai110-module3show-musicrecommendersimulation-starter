import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

# Columns that must be numbers so we can do math on them later.
INT_FIELDS = {"id"}
FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV into a list of dicts, converting numeric columns to numbers."""
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip fully blank lines (e.g. a trailing newline in the file).
            if not any((value or "").strip() for value in row.values()):
                continue

            song: Dict = {}
            for key, value in row.items():
                value = (value or "").strip()
                if key in INT_FIELDS:
                    song[key] = int(value)
                elif key in FLOAT_FIELDS:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

# --- Algorithm Recipe weights (see README "Finalized Algorithm Recipe") ---
GENRE_WEIGHT = 3.0        # exact match: genre leads
MOOD_WEIGHT = 2.0         # exact match: vibe tier
ENERGY_WEIGHT = 2.0       # closeness: vibe tier
VALENCE_WEIGHT = 1.0      # closeness: optional refiner
ACOUSTICNESS_WEIGHT = 1.0  # closeness: optional refiner


def _closeness(song_value: float, target_value: float, weight: float) -> float:
    """Reward proximity to a 0-1 target: full weight at an exact match, dropping to 0 as values diverge."""
    distance = abs(song_value - target_value)
    return weight * (1 - distance)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs, returning (total score, list of reason strings)."""
    score = 0.0
    reasons: List[str] = []

    # --- Categorical rules: exact match awards full points ---
    if user_prefs.get("genre") and song.get("genre") == user_prefs["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({song['genre']}) (+{GENRE_WEIGHT})")

    if user_prefs.get("mood") and song.get("mood") == user_prefs["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({song['mood']}) (+{MOOD_WEIGHT})")

    # --- Numeric rules: closeness to the user's target (1 - |difference|) ---
    if "energy" in user_prefs:
        points = _closeness(song["energy"], user_prefs["energy"], ENERGY_WEIGHT)
        score += points
        reasons.append(f"energy close to {user_prefs['energy']} (+{points:.2f})")

    if "valence" in user_prefs:
        points = _closeness(song["valence"], user_prefs["valence"], VALENCE_WEIGHT)
        score += points
        reasons.append(f"valence close to {user_prefs['valence']} (+{points:.2f})")

    if "acousticness" in user_prefs:
        points = _closeness(
            song["acousticness"], user_prefs["acousticness"], ACOUSTICNESS_WEIGHT
        )
        score += points
        reasons.append(f"acousticness close to {user_prefs['acousticness']} (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest-first, and return the top k as (song, score, explanation) tuples."""
    # 1. JUDGE: score every single song in the catalog.
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no matching preferences"
        scored.append((song, score, explanation))

    # 2. RANK: sort by score, highest first.
    scored.sort(key=lambda item: item[1], reverse=True)

    # 3. TRIM: return only the top k.
    return scored[:k]
