# Aquila Auto-Resolve — 5-Minute Presentation Script

> Speak casually, like you're explaining it to Mahdi. Pause at the [brackets]. Total ~700 words = 5 min.

---

**[0:00–0:45] Intro**

Hey, I'm Jason. For my IAT 461 final I worked with Mahdi from Ballista Games on their game Aquila. The thing we looked at is the auto-resolve button, the one that decides a battle without you playing it out. [pause] Players use it a lot, but they don't really trust it, because right now it only gets the winner right about 63 percent of the time. So the question was: can we rebuild that button from the battle data so it's actually accurate?

---

**[0:45–1:30] Why it matters**

The reason this matters is the player experience. When the button says "you won" and you didn't, or vice versa, people stop using it, or they get annoyed and replay every fight by hand. [pause] And that's a real cost, because in a game with this many battles, nobody wants to manually play all of them. So the goal wasn't to remove auto-resolve, it was to make the prediction good enough that players trust it.

---

**[1:30–2:30] The three options**

In my proposal I laid out three options. [pause] Option A was just remove the button entirely. But the data killed that immediately, players auto-resolve 72 percent of battles, so taking it away forces everyone to play everything by hand. Off the table. Option B was a flat rule, like "whoever has more troops wins." Sounds reasonable, but it only hits about 63 percent, same as the current engine, so it's not actually a fix. [pause] That leaves Option C, rebuild the resolver from the battle data using a model. And that's what the numbers supported, so that's what I built.

---

**[2:30–3:45] The model and results**

I used a plain logistic regression. Kept it simple on purpose, because the client needs to read the weights and rebalance the game from them. [pause] On battles the model has never seen, it predicts the winner about 80 percent of the time, and about 81 percent under cross-validation. Both beat the current 63 percent. [pause] And it's readable, the model leans on cavalry and shock troops for the attacker, and on spears and fortifications for the defender. So a designer can look at those weights and actually tune the units. The other piece is a confidence score, so the game can auto-resolve the lopsided matches and just hand the close ones back to the player.

---

**[3:45–4:15] Unit role audit**

The second part was the unit role audit. Mahdi's marketing labels split units into six groups, and we wanted to check those labels still match what the unit descriptions actually say. [pause] I used TF-IDF plus KMeans on the descriptions, and the clusters agreed with the labels about 82.5 percent of the time. So the labels mostly hold up, with just a few fuzzy ones, like the Skirmisher-Missile and Cavalry-Shock overlap, worth a designer taking a second look at.

---

**[4:15–4:45] Limitations**

Quick on limitations. The data is one synthetic simulation, so 80 percent might not carry over to a live build. Battles aren't time-stamped, so I used random splits, not a real forecast. And the app's predictions are in-sample, so they're illustrative, not a validated forecast. [pause] I called that out honestly rather than overselling it.

---

**[4:45–5:00] Close + demo**

So that's the project: a rebuild of the auto-resolve button that beats the old one, plus a check on the unit labels. [pause] And here's the app, you can punch in a battle and see the prediction and the confidence. Thanks.

---

## Recording notes
- Open the Streamlit app (the live link) before recording so you can show it at the end.
- Keep it to one take per section; you can splice.
- Don't read the numbers robotically, say them like "about eighty percent, beats the sixty-three."
- Save the final as `Aquila_Presentation.mp4` in this folder, then I'll flip the README from TBA to the link.
