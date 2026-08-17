# Aquila Auto-Resolve Battle Engine

IAT 461 final project, Summer 2026
Data scientist: Jason Salonga (301400669)
Client: Mahdi Taziki (301373483), Ballista Games / Aquila studio

This project looks at whether the battle data behind a strategy game's auto-resolve button can be used to rebuild that button so it predicts the winner more accurately. The studio ships an auto-resolve feature that decides battles without playing them out, and players do not trust it because it is only right about 63 percent of the time. The final output is a readable logistic-regression model that beats that bar, plus a confidence score the game can use to auto-resolve only the lopsided matches.

## Submission links

- **Recorded presentation:** Aquila_Presentation.mp4 (add before submitting)
- **Streamlit app:** [deployment pending, slither.cc subdomain](https://github.com/jasonsalonga/Aquila-Auto-Resolve)
- **Final notebook:** [`notebooks/01_Aquila_Final.ipynb`](notebooks/01_Aquila_Final.ipynb)
- **Final report:** [`FINAL_REPORT_AUG_17.pdf`](FINAL_REPORT_AUG_17.pdf)

## Project files

- [`notebooks/01_Aquila_Final.ipynb`](notebooks/01_Aquila_Final.ipynb) contains the full analysis: the problem restatement, data documentation, assumptions log, Option A/B/C comparison, the logistic-regression model, the unit role audit, limitations, and the executive summary.
- [`FINAL_REPORT_AUG_17.pdf`](FINAL_REPORT_AUG_17.pdf) is the PDF export of that notebook.
- [`streamlit_app.py`](streamlit_app.py) is the interactive version of the battle predictor and the unit role auditor (the plus 10 percent bonus).
- [`battles.csv`](battles.csv) holds 1,000 simulated battles from the auto-resolve engine, one row per battle.
- [`unit_roster.csv`](unit_roster.csv) holds 240 units with a marketing label and a free-text description.
- [`Phase1_ClientProposal.pdf`](Phase1_ClientProposal.pdf) is the client brief written for Mahdi.
- [`requirements.txt`](requirements.txt) lists the Python packages needed to run the notebook and app.

## Decisions from the client check-in

The Phase 1 proposal frames three options: remove auto-resolve, patch it with a flat troop-count rule, or rebuild it from the battle data. The data answered two of those directly. Players auto-resolve 72 percent of battles, so removing the button would force everyone to play every fight by hand, which is off the table. A flat "more troops wins" rule does no better than the current engine's 63 percent, so that is not the fix either. That left rebuilding the resolver as Option C, which the model supports.

The client also confirmed the outcome column is ground truth. I predict `outcome`, not the engine's own call, and I treat faction names as categorical identifiers rather than predictive features so the model does not overfit to specific matchups. The 16 troop columns plus general ratings, morale, fatigue, fortification, and reinforcement timing are the usable signal.

For the unit role audit, the client's marketing labels have six groups. I used TF-IDF plus KMeans to check whether those six labels still match the unit descriptions, and treated 82.5 percent agreement as the threshold for "holds up."

## Results

The auto-resolve button is used in 72 percent of battles, so removing it is off the table. A simple "more troops wins" rule reaches about the same 63 percent as the current engine, so that is not the fix either.

A plain logistic-regression model predicts the winner about 80 percent of the time on battles it has never seen, and about 81 percent under cross-validation, beating the current engine's 63 percent. The model is readable: it leans on cavalry and shock troops for the attacker, and on spears and fortifications for the defender, so a designer can rebalance from the weights. Its confidence score lets the game auto-resolve the lopsided matches and hand the close ones back to the player.

For the unit role audit, the six marketing labels hold up well, with 82.5 percent agreement between the clusters and the labels. Only a few borderline units (for example the fuzzy Skirmisher/Missile and Cavalry/Shock groups) are worth a designer's second look.

## Main limitations

- The dataset is a single synthetic game simulation, so the 80 percent accuracy may not transfer to a live player build. There are no real player battles and no future outcomes to validate against.
- Battles are not time-stamped, so we use stratified random splits rather than a true temporal holdout. A deployable resolver would need a forecasting split.
- The role audit uses shallow text modelling (TF-IDF plus KMeans), which catches vocabulary clusters but not deeper semantics. A transformer embedding could refine the fuzzy groups.
- The model scores are in-sample for any battle that was also a training example, so the Streamlit app's predictions on the supplied data are illustrative, not a validated forecast.

## Repository contents

```text
notebooks/01_Aquila_Final.ipynb     final analysis (Tasks 1 to 3)
FINAL_REPORT_AUG_17.pdf             PDF export of the notebook
streamlit_app.py                    interactive battle predictor and unit role auditor
battles.csv                         1,000 simulated battles
unit_roster.csv                     240 units with marketing labels
Phase1_ClientProposal.pdf           client proposal
requirements.txt                    Python packages
README.md                           this file
```

## Running the project

Install the packages from the repository root:

```bash
pip install -r requirements.txt
```

Run the notebook from the notebooks folder:

```bash
cd notebooks
jupyter lab
```

The final notebook reads `../battles.csv` and `../unit_roster.csv` and reproduces the Option A/B/C comparison, the logistic-regression model, and the unit role audit.

Run the app from the repository root:

```bash
streamlit run streamlit_app.py
```

The app needs `battles.csv` and `unit_roster.csv` in the same folder.
