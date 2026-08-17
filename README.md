# Aquila Auto-Resolve Battle Engine, Final Project

**IAT 461, Summer 2026: Final Project**
Student (data scientist): Jason Salonga (#301400669)
Client: Mahdi Taziki (Ballista Games / Aquila studio)

## The problem and method choice

The client runs a strategy game studio called Aquila and ships an auto-resolve button that decides who wins a battle without playing it out. Players do not trust the button. The studio asked three questions: should we remove auto-resolve, patch it with a simple rule, or rebuild it from the battle data. The current engine is right only 63 percent of the time, which is the bar to beat.

This is a supervised classification task. The label is the actual battle winner, and the features are troop types, commander skill, morale, terrain, and weather. I used logistic regression because it is readable by a game designer who wants to rebalance from the weights. I checked the result honestly with cross-validation and a held-out test set, and I built a confidence score so the game can auto-resolve only the lopsided matches.

## What this repo contains

- `notebooks/Aquila_Final.ipynb` - the full analysis (data loading, Tasks 1 to 3, conclusion, 0 errors)
- `streamlit_app.py` - interactive battle predictor and unit role auditor (the plus 10 percent bonus)
- `battles.csv`, `unit_roster.csv` - the source data
- `Phase1_ClientProposal.pdf` - the client brief I wrote for Mahdi
- `Client_Evaluation_Report.docx` - my Phase 4 evaluation of Mahdi's solution to my brief
- `Final_Report.pdf` - PDF export of the notebook
- `Aquila_Presentation.mp4` - the 5 minute presentation (add before submitting)

## How to run

The notebook runs top to bottom in Jupyter. The Streamlit app needs the two CSV files in the same folder:

```
pip install streamlit scikit-learn pandas matplotlib
streamlit run streamlit_app.py
```
