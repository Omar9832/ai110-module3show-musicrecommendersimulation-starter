"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Three distinct listener profiles to try against the catalog.
USER_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4, "acousticness": 0.8},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.4},
}


def show_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top-k recommendations for one named profile in a clean layout."""
    prefs_summary = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print()
    print("=" * 52)
    print(f"  {name.upper()}")
    print(f"  Likes: {prefs_summary}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=k), start=1
    ):
        print(f"\n  {rank}. {song['title']}  -  {song['artist']}")
        print(f"     Score: {score:.2f}")
        print("     Because:")
        for reason in explanation.split("; "):
            print(f"       - {reason}")

    print("\n" + "=" * 52)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in USER_PROFILES.items():
        show_recommendations(name, user_prefs, songs, k=3)


if __name__ == "__main__":
    main()
