"""Simulate a chord-tension rating experiment.

Design
------
- 24 participants (P01-P24)
- 7 chord types, each presented 5 times per participant (35 trials each,
  randomised order) -> 840 trials total
- Dissonance is operationalised as spectral roughness (0-1, higher = more
  dissonant; roughly the Hutchinson-Knopoff / Plomp-Levelt family of measures
  rescaled to 0-1). Each chord type has a baseline value, and the dissonance
  as presented increases slightly with loudness (~55-85 dB SPL, varied per
  trial).
- Tension ratings are continuous, 0-100 (visual-analogue slider), generated
  from a linear model:
      rating = b0 + b1*dissonance + b2*(loudness-70)/10
               + participant_intercept + noise
  then clipped to the 0-100 scale.

Run:  python generate_data.py   (writes data/chord_tension_ratings.csv)
"""

from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(seed=2026)

N_PARTICIPANTS = 24
N_REPS = 5  # presentations of each chord type per participant

# chord type -> baseline dissonance (spectral roughness, 0-1)
CHORDS = {
    "Major":               0.08,
    "minor":               0.14,
    "major-seventh":       0.18,
    "dominant-seventh":    0.32,
    "half-diminished":     0.45,
    "augmented":           0.50,
    "diminished-seventh":  0.55,
}

# generative model coefficients (on the 0-100 rating scale)
B0 = 5.0            # baseline tension for a perfectly consonant chord at 70 dB
B_DISSONANCE = 85.0 # effect of presented dissonance (spectral roughness)
B_LOUDNESS = 9.0    # effect per +10 dB
SD_PARTICIPANT = 8.0
SD_NOISE = 12.0


def main() -> None:
    participant_ids = [f"P{i:02d}" for i in range(1, N_PARTICIPANTS + 1)]
    intercepts = dict(zip(participant_ids, RNG.normal(0.0, SD_PARTICIPANT, N_PARTICIPANTS)))

    rows = []
    for pid in participant_ids:
        # build this participant's randomised trial list
        trial_chords = np.repeat(list(CHORDS.keys()), N_REPS)
        RNG.shuffle(trial_chords)
        for trial, chord in enumerate(trial_chords, start=1):
            base_dissonance = CHORDS[chord]
            loudness = np.round(RNG.uniform(55, 85), 1)
            # roughness (= dissonance) grows slightly with level (~1% per dB above 70)
            dissonance = np.clip(base_dissonance * (1 + 0.01 * (loudness - 70)), 0, 1)

            latent = (
                B0
                + B_DISSONANCE * dissonance
                + B_LOUDNESS * (loudness - 70) / 10
                + intercepts[pid]
                + RNG.normal(0.0, SD_NOISE)
            )
            rating = round(float(np.clip(latent, 0, 100)), 1)

            rows.append(
                {
                    "trial": trial,
                    "participant_id": pid,
                    "chord_type": chord,
                    "tension_rating": rating,
                    "dissonance": round(float(dissonance), 3),
                    "loudness_db": loudness,
                }
            )

    df = pd.DataFrame(rows)
    out = Path(__file__).parent / "data" / "chord_tension_ratings.csv"
    out.parent.mkdir(exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} trials for {N_PARTICIPANTS} participants -> {out}")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
