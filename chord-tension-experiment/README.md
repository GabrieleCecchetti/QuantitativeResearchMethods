# Chord Tension Experiment (simulated)

Simulated data and analysis notebook for an experiment in which participants
hear isolated chords and rate the tension they feel on a continuous 0–100
scale (visual-analogue slider).

## Contents

| File | What it is |
|---|---|
| `data/chord_tension_ratings.csv` | 840 trials: 24 participants × 7 chord types × 5 repetitions |
| `generate_data.py` | Script that simulated the data (seeded, so re-running reproduces the same CSV) |
| `chord_tension_analysis.ipynb` | Analysis notebook: data inspection, interactive per-participant plots, regression |

## Data columns

| Column | Meaning |
|---|---|
| `trial` | Trial number within a participant's session (1–35, randomised order) |
| `participant_id` | Participant code (P01–P24) |
| `chord_type` | Chord presented (Major, minor, augmented, major-seventh, dominant-seventh, diminished-seventh, half-diminished) |
| `tension_rating` | Tension rating, continuous 0 (relaxed) – 100 (very tense) |
| `dissonance` | Dissonance of the chord as presented, operationalised as spectral roughness (0–1, higher = more dissonant; increases slightly with loudness) |
| `loudness_db` | Presentation level in dB SPL (~55–85) |

## How the data were simulated

Tension is generated from a linear model — it increases with dissonance
(spectral roughness) and loudness, plus a random intercept per
participant and trial-level noise — then clipped to the 0–100 scale.
Coefficients are at the top of `generate_data.py` if you want to change the
effect sizes, sample size, or chord set.

## Running the notebook

Requires `pandas`, `numpy`, `matplotlib`, `scipy`, and `ipywidgets` (for the
participant dropdown). Open `chord_tension_analysis.ipynb` in Jupyter and run
all cells; the interactive plot needs a live kernel to respond to the dropdown.
