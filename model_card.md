# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

It matches a listener to songs that fit their vibe.

---

## 2. Intended Use  

This is a small demo recommender for a class project. You give it a taste profile, like a genre, a mood, and an energy level. It gives back a few songs that fit, with a short reason for each pick.

It assumes the user can describe their taste in simple words. It also assumes the labels in the data are correct.

What it should not be used for:

- It is not a real product. Don't use it to power a real app.
- It only knows the 18 songs in the file. It can't suggest anything else.
- It doesn't actually listen to the music. It only reads the labels. So don't trust it for careful taste decisions.

---

## 3. How the Model Works  

Each song has a genre, a mood, and some number features like energy and acousticness. The user gives their own version of these: a favorite genre, a favorite mood, and target numbers.

The model gives each song points. A matching genre is worth the most, 3 points. A matching mood is next, 2 points. For the number features, it checks how close the song is to what the user asked for. A close match earns more points. A far match earns less.

Then it adds up the points for every song. It sorts them from highest to lowest and shows the top few. Each song also comes with a short list of reasons, so you can see why it was picked.

While testing, I tried doubling the energy weight and halving the genre weight. It didn't really help, so I put the weights back where they started.

---

## 4. Data  

The catalog has 18 songs. Each song has a title, artist, genre, and mood. It also has five number features: energy, tempo, valence, danceability, and acousticness. All the numbers except tempo are between 0 and 1.

There are 15 genres and 14 moods. Most of them only show up once. Lofi has three songs and pop has two. Everything else has just one.

I didn't add or remove any songs. The dataset is small, so it doesn't cover much. There are no medium-energy songs, and no loud acoustic songs. A lot of real taste is just missing.

---

## 5. Strengths  

The system works best when the user's exact genre and mood are in the data. Then the right song jumps to the top with a clear lead.

Chill Lofi was the strongest example. The top three were all the lofi tracks, in an order that made sense to me.

It also gives a reason for every pick. That makes it easy to see why a song was chosen, and easy to spot when something looks wrong.

The number features work too. Energy sorts songs into calm and hyped. Valence splits happy from dark. When I compared profiles, these features clearly changed the results in ways that made sense.

---

## 6. Limitations and Bias 

One clear weakness I found is an "energy gap." When I sorted every song by energy, the catalog split into two groups: ten low-energy songs from 0.28 to 0.50, and eight high-energy songs from 0.75 to 0.97. Nothing sits in between. Since my scoring is based on how close a song's energy is to what the user asked for, someone who wants moderate energy around 0.6 can never score higher than 1.80 out of 2.0, while someone who wants 0.4 or 0.9 gets almost a perfect 2.0. The system doesn't flag this either. It just returns whichever cluster is a little closer, so the most average listener actually ends up with the worst matches. This is more of a data problem than a math problem, so the fix would be adding some mid-energy songs rather than changing the weights.

---

## 7. Evaluation  

I tested the recommender in a few ways. First I ran the three built-in profiles (High-Energy Pop, Chill Lofi, and Deep Intense Rock) and read through the top results to see if they matched what I would have picked myself. Chill Lofi looked the best, since the top three were all the lofi tracks in a sensible order, and the other two profiles got the obvious #1 right as well.

Then I built a set of "trick" profiles to see where the scoring would break, and a few of the results surprised me. When I typed a genre or mood that isn't in the catalog, like "trap" or "sad", the system didn't warn me at all and just ranked everything by energy instead. When I set energy above 1.0 or below 0, the closeness math went negative and even printed a strange "+-0.10" in the reasons. And when I asked for high energy and high acousticness together, it still returned songs that were the opposite of acoustic, because no song in the catalog is both.

The most useful test was sorting every song by energy, which is how I found the energy gap described above. I didn't use any formal metrics for this project. I mostly compared the output against my own taste and looked for rankings that clearly felt wrong.

To check that each preference was actually doing something, I also compared the three profiles against each other, two at a time:

- **High-Energy Pop vs. Chill Lofi:** These two share no songs at all. Pop targets energy 0.9 and its top picks sit between 0.76 and 0.93, while Lofi targets 0.4 and its picks sit between 0.35 and 0.42. Lofi also asks for high acousticness (0.8), so it pulls in quiet, acoustic tracks (acousticness around 0.71 to 0.86), while the Pop list is full of electronic tracks (acousticness 0.05 to 0.35). This is what I expected, since the two profiles are close to opposites, so their outputs shouldn't overlap.

- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy (0.9), so their candidate pools overlap, and Gym Hero actually shows up as #2 in both lists because it is high-energy and fits part of each one. What separates them is mood and valence. Pop wants happy, so its #1 is the bright, upbeat Sunrise City (valence 0.84). Rock wants intense with a lower valence of 0.4, so its #1 is the darker Storm Runner (valence 0.48). It's the same energy zone, but valence is what splits "bright and happy" from "intense and dark," which tells me that feature is doing real work.

- **Chill Lofi vs. Deep Intense Rock:** This is the biggest contrast of the three. Energy goes from 0.4 up to 0.9, acousticness from high to low, genre from lofi to rock, and mood from chill to intense. The Lofi list is quiet and acoustic (energy around 0.4, acousticness around 0.8) and the Rock list is loud and electronic (energy around 0.9, acousticness around 0.10). Nothing appears in both, which makes sense because almost every preference is flipped.

The thing that surprised me most here was seeing Gym Hero land in two different lists. Once I looked at why, it made sense: it earns most of its points from energy (0.93, close to the 0.9 both profiles asked for), not from genre. So the little bit of repetition across profiles comes from the energy rule, not from a genre bias.

---

## 8. Future Work  

- Add more songs, especially medium-energy ones. That would close the energy gap.
- Give partial credit for similar genres. Right now rock and metal count as totally different. A rock fan might like metal, but the system can't see that.
- Check the user's input. If someone types a genre that doesn't exist, or an energy above 1, the system should warn them instead of giving quiet, wrong results.

---

## 9. Personal Reflection  

My biggest learning moment was finding the energy gap. I only found it because I stopped staring at the code and looked at the data instead. I sorted every song by energy and saw the hole in the middle. The scoring math was fine. The problem was the song list. That taught me to check the data, not just the logic.

AI tools helped me a lot during this. They wrote small scripts to sort the songs and run the trick profiles for me. They also explained the scoring math when I wasn't sure how a score was built. That saved me time and helped me test more ideas than I would have alone.

But I learned to double-check them. When the AI told me a ranking, I re-ran the program myself to see the real output. A few times I checked a score by hand to make sure the numbers matched. I also had to rewrite a lot of the AI's text, because it didn't sound like me at first. So I used it as a helper, not as the final answer.

What surprised me most was how a simple algorithm can still feel like a real recommendation. In the end it just adds up points and sorts a list. There is no smarts in it. But because it shows a reason for every pick, it feels like it understands your taste. That made me realize how much of the "magic" in real apps might just be clear explanations on top of basic math.

If I kept going, I would add more songs to fill the gaps, give partial credit for similar genres, and add input checks so bad input doesn't give quiet, wrong results. I'd also like to let a user mix two tastes at once and see how the system handles it.

Now I think about real music apps differently. If the math and data have blind spots this easily, big apps must have them too. They are just harder to see.
