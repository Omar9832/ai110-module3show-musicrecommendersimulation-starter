# 🎵 Music Recommender Simulation

## Project Summary

This is a small music recommender called VibeMatch 1.0. You give it a taste profile, like a favorite genre, a mood, and a target energy level. It scores every song in a small catalog against your taste, ranks them, and returns the best few. Each pick also comes with a short reason so you can see why it was chosen.

The point of the project wasn't just to make it work. It was to look closely at what the system gets right and wrong, find the biases hiding in the scoring and the data, and reflect on how the same problems show up in real recommender apps.

---

## How The System Works

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

## Adversarial / Edge-Case Profiles

I made seven "trick" profiles to try to break the scoring or catch it doing
something odd. Below is the real terminal output (top 5 with explanations) for
each one.

**A. Typo / nonexistent categories.** If the genre or mood isn't in the catalog, the
system just ignores it with no warning and ranks everything by energy instead.

```
A. Typo / nonexistent categories
prefs: {'genre': 'trap', 'mood': 'sad', 'energy': 0.5}
----------------------------------------------------------------
  1.   2.00  Island Time            [reggae/serene e=0.5]
          because: energy close to 0.5 (+2.00)
  2.   1.96  Velvet Hours           [r&b/romantic e=0.48]
          because: energy close to 0.5 (+1.96)
  3.   1.90  Dust and Highways      [country/nostalgic e=0.45]
          because: energy close to 0.5 (+1.90)
  4.   1.84  Midnight Coding        [lofi/chill e=0.42]
          because: energy close to 0.5 (+1.84)
  5.   1.84  Paper Boats            [folk/hopeful e=0.42]
          because: energy close to 0.5 (+1.84)
```

**B. Conflict: max energy + melancholy classical.** A genre and mood match is worth 5
points, which is more than all the numeric rules combined, so the lowest-energy song
wins even though I asked for maximum energy.

```
B. Conflict: max energy + melancholy classical
prefs: {'genre': 'classical', 'mood': 'melancholy', 'energy': 0.95}
----------------------------------------------------------------
  1.   5.70  Winter Elegy           [classical/melancholy e=0.3]
          because: genre match (classical) (+3.0); mood match (melancholy) (+2.0); energy close to 0.95 (+0.70)
  2.   2.00  Neon Sunrise           [edm/euphoric e=0.95]
          because: energy close to 0.95 (+2.00)
  3.   1.96  Gym Hero               [pop/intense e=0.93]
          because: energy close to 0.95 (+1.96)
  4.   1.96  Iron Verdict           [metal/angry e=0.97]
          because: energy close to 0.95 (+1.96)
  5.   1.92  Storm Runner           [rock/intense e=0.91]
          because: energy close to 0.95 (+1.92)
```

**C. Impossible combo: high energy + very acoustic.** No song is both, so the top 5
are almost tied and the tiny acousticness differences decide the order. The reasons
still say "acousticness close to 0.95" even for songs that are barely acoustic.

```
C. Impossible combo: high energy + very acoustic
prefs: {'energy': 0.95, 'acousticness': 0.95}
----------------------------------------------------------------
  1.   2.07  Storm Runner           [rock/intense e=0.91]
          because: energy close to 0.95 (+1.92); acousticness close to 0.95 (+0.15)
  2.   2.07  Neon Sunrise           [edm/euphoric e=0.95]
          because: energy close to 0.95 (+2.00); acousticness close to 0.95 (+0.07)
  3.   2.06  Gym Hero               [pop/intense e=0.93]
          because: energy close to 0.95 (+1.96); acousticness close to 0.95 (+0.10)
  4.   2.05  Iron Verdict           [metal/angry e=0.97]
          because: energy close to 0.95 (+1.96); acousticness close to 0.95 (+0.09)
  5.   2.02  Rooftop Lights         [indie pop/happy e=0.76]
          because: energy close to 0.95 (+1.62); acousticness close to 0.95 (+0.40)
```

**D. Out-of-range target (energy=2.0).** There is no input checking, so the closeness
formula goes negative and even prints a broken `+-0.10` in the reasons. Only the genre
match keeps one song positive.

```
D. Out-of-range target (energy=2.0)
prefs: {'genre': 'edm', 'energy': 2.0}
----------------------------------------------------------------
  1.   2.90  Neon Sunrise           [edm/euphoric e=0.95]
          because: genre match (edm) (+3.0); energy close to 2.0 (+-0.10)
  2.  -0.06  Iron Verdict           [metal/angry e=0.97]
          because: energy close to 2.0 (+-0.06)
  3.  -0.14  Gym Hero               [pop/intense e=0.93]
          because: energy close to 2.0 (+-0.14)
  4.  -0.18  Storm Runner           [rock/intense e=0.91]
          because: energy close to 2.0 (+-0.18)
  5.  -0.30  Concrete Kings         [hip hop/aggressive e=0.85]
          because: energy close to 2.0 (+-0.30)
```

**E. Negative target (energy=-1.0).** Every score turns negative and the ranking flips,
so the lowest-energy song is now counted as the closest match.

```
E. Negative target (energy=-1.0)
prefs: {'energy': -1.0}
----------------------------------------------------------------
  1.  -0.56  Spacewalk Thoughts     [ambient/chill e=0.28]
          because: energy close to -1.0 (+-0.56)
  2.  -0.60  Winter Elegy           [classical/melancholy e=0.3]
          because: energy close to -1.0 (+-0.60)
  3.  -0.70  Library Rain           [lofi/chill e=0.35]
          because: energy close to -1.0 (+-0.70)
  4.  -0.74  Coffee Shop Stories    [jazz/relaxed e=0.37]
          because: energy close to -1.0 (+-0.74)
  5.  -0.80  Focus Flow             [lofi/focused e=0.4]
          because: energy close to -1.0 (+-0.80)
```

**F. Empty prefs (no signal at all).** With no preferences given, every song scores
0.00, so the "top 5" is just the first five rows of the CSV in file order.

```
F. Empty prefs (no signal at all)
prefs: {}
----------------------------------------------------------------
  1.   0.00  Sunrise City           [pop/happy e=0.82]
          because: no matching preferences
  2.   0.00  Midnight Coding        [lofi/chill e=0.42]
          because: no matching preferences
  3.   0.00  Storm Runner           [rock/intense e=0.91]
          because: no matching preferences
  4.   0.00  Library Rain           [lofi/chill e=0.35]
          because: no matching preferences
  5.   0.00  Gym Hero               [pop/intense e=0.93]
          because: no matching preferences
```

**G. Genre-only steamroller.** A genre-only search gives every matching song the same
3.00, so the order within the genre comes down to nothing but CSV row order.

```
G. Genre-only steamroller
prefs: {'genre': 'lofi'}
----------------------------------------------------------------
  1.   3.00  Midnight Coding        [lofi/chill e=0.42]
          because: genre match (lofi) (+3.0)
  2.   3.00  Library Rain           [lofi/chill e=0.35]
          because: genre match (lofi) (+3.0)
  3.   3.00  Focus Flow             [lofi/focused e=0.4]
          because: genre match (lofi) (+3.0)
  4.   0.00  Sunrise City           [pop/happy e=0.82]
          because: no matching preferences
  5.   0.00  Storm Runner           [rock/intense e=0.91]
          because: no matching preferences
```

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

The full reflection is in the model card: [**Model Card**](model_card.md).

Working on this showed me that a recommender is just data turned into numbers and sorted. The system doesn't "know" music. It gives points for matching a genre or mood, measures how close each song's energy is to what you asked for, adds it all up, and ranks the list. That is the whole prediction. It only feels smart because it shows a reason for every pick.

It also showed me how easily bias sneaks in. My catalog had three lofi songs but only one metal song, so lofi fans get more choices than metal fans. There was also an energy gap in the middle of the data, which quietly gave average listeners the worst matches. None of that was on purpose. It came from the shape of the data, which is exactly how unfairness can hide in bigger systems too.



