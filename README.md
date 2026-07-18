# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

My recommender is a content-based system that works entirely off the attributes of each song. Every `Song` carries a genre, a mood, and four numeric "vibe" features from the dataset: energy, valence, danceability, and acousticness (plus tempo in beats per minute, which I left out of the score because energy already captures most of what it tells me). The `UserProfile` stores what a listener is looking for — a favorite genre, a favorite mood, and a target energy level between 0 and 1 — which is basically a description of the kind of song they want to hear right now. To score a single song, the `Recommender` adds up points from a few weighted rules: it gives the biggest reward (3 points) when the genre matches, a solid reward (2 points) when the mood matches, and for energy it measures how *close* the song is to the user's target rather than just favoring high or low values, using `2 × (1 − |song_energy − target_energy|)` so a perfect match earns full points and songs drift toward zero as they move away. Every rule that fires also records a short reason, which is what lets the system explain itself. Finally, to choose what to actually recommend, I score every song in the catalog, sort them from highest to lowest, and return the top few — so the recommendations are simply the songs that best matched the listener's taste, in order.

### Finalized Algorithm Recipe

Each song starts at 0 points and earns points from these rules (higher total = better match):

| Rule | Type | Points |
|------|------|--------|
| Genre matches the user's favorite genre | exact match | **+3.0** |
| Mood matches the user's favorite mood | exact match | **+2.0** |
| Energy is close to the user's target | closeness | **+2.0 × (1 − \|song_energy − target_energy\|)** |
| Valence is close to the user's target *(optional refiner)* | closeness | **+1.0 × (1 − \|song_valence − target_valence\|)** |
| Acousticness is close to the user's target *(optional refiner)* | closeness | **+1.0 × (1 − \|song_acousticness − target_acousticness\|)** |

The weights form tiers on purpose: **genre (3) leads**, the **vibe features — mood and energy (2 each) — come second**, and valence/acousticness (1 each) only fine-tune the order. The spacing guarantees a correct-genre song can never be beaten by a wrong-genre song that happens to match the smaller features. After scoring, the list is sorted high-to-low and trimmed to the top *k*.

### Potential Biases

- **Genre over-prioritization.** Because genre carries the most weight, the system can bury a song that perfectly matches the user's mood and energy just because its genre label is different — so it may miss great cross-genre recommendations.
- **Popularity/catalog bias.** Scoring only compares against the songs in this tiny CSV, so a "best" recommendation is only best *relative to a handful of tracks*, not to music broadly.
- **Filter-bubble effect.** Content-based scoring keeps suggesting more of what the user already likes and rarely surprises them, which can trap a listener in a narrow slice of their taste.
- **No understanding of the actual audio, lyrics, or language.** The system trusts the numeric labels; if those labels are wrong or biased, the recommendations inherit that bias.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Below is the actual terminal output from `python -m src.main` for the default
`genre=pop, mood=happy, energy=0.8` profile:

```
Loaded songs: 18

====================================================
  TOP RECOMMENDATIONS
  For a listener who likes: genre=pop, mood=happy, energy=0.8
====================================================

  1. Sunrise City  -  Neon Echo
     Score: 6.96
     Because:
       - genre match (pop) (+3.0)
       - mood match (happy) (+2.0)
       - energy close to 0.8 (+1.96)

  2. Gym Hero  -  Max Pulse
     Score: 4.74
     Because:
       - genre match (pop) (+3.0)
       - energy close to 0.8 (+1.74)

  3. Rooftop Lights  -  Indigo Parade
     Score: 3.92
     Because:
       - mood match (happy) (+2.0)
       - energy close to 0.8 (+1.92)

  4. Concrete Kings  -  Blok Theory
     Score: 1.90
     Because:
       - energy close to 0.8 (+1.90)

  5. Night Drive Loop  -  Neon Echo
     Score: 1.90
     Because:
       - energy close to 0.8 (+1.90)

====================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



