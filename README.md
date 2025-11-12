# HeHeHaHa DataRoyale 🏆

> Comprehensive analysis of 16+ million Clash Royale battles from December 2020

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Chau-Nguyen-Developer/HeHeHaHa_DataRoyale/blob/main/Chau_RoyaleClash.ipynb)

## Overview

This repository contains analysis of a massive Clash Royale battle dataset with **16.3 million battles** (32.6M player-match records) collected over 11-12 days in December 2020. The dataset provides deep insights into player behavior, clan dynamics, card meta, and competitive patterns.

### Quick Stats

| Metric | Value |
|--------|-------|
| 📊 Total Battles | 16,304,356 |
| 👥 Player Records | 32,608,712 |
| 🏰 Unique Clans | ~395,000 |
| 📁 Dataset Size | 9.87 GB |
| 📅 Time Period | Dec 7-18, 2020 |
| 🎯 Game Mode | Ladder (72000201) |

## Key Findings 🔍

### 🚨 The Clan Engagement Crisis

Our analysis uncovered a **startling retention problem**:

- **49.2%** of clans appear in only ONE match
- Of those single-match clans, **97.96% LOST**
- Suggests players join/create clans, lose a match, and immediately abandon

### 🎮 Competitive Balance

The trophy system is remarkably well-balanced:
- Winners gain average **+29.4** trophies
- Losers lose average **-29.4** trophies
- Peak activity: **4,000-6,000** trophy range (63% of battles)

### 🃏 Deck Meta

**Winning deck characteristics:**
- Average elixir: **3.84** (same as losers - cost doesn't predict wins!)
- Card composition: **5-6 troops, 0-1 structures, 2 spells**
- Card levels: **95-96** total (out of max 104)
- Most common victory: **2 crowns** (1.77 avg vs 0.93)

## Repository Structure

```
HeHeHaHa_DataRoyale/
├── Chau_RoyaleClash.ipynb          # Original exploratory analysis (800k sample)
├── full_dataset_analysis.py        # Complete dataset analysis script
├── dataset_estimation_analysis.py  # Quick insights without downloading data
├── FULL_DATASET_ANALYSIS.md        # Comprehensive findings report
└── README.md                        # This file
```

## Getting Started

### Option 1: Quick Overview (No Download Required)

```bash
python dataset_estimation_analysis.py
```

This provides comprehensive insights extrapolated from the 800k sample without needing to download the 9.87GB dataset.

### Option 2: Full Analysis

**Step 1: Download the dataset**

```bash
pip install gdown
gdown 1sgMvwiuZNyBt86JD3FRVZa5YRi6DpbBj
```

Or download manually: [Google Drive Link](https://drive.google.com/file/d/1sgMvwiuZNyBt86JD3FRVZa5YRi6DpbBj/view?usp=drive_link)

**Step 2: Run full analysis**

```bash
pip install pandas numpy
python full_dataset_analysis.py
```

**System Requirements:**
- RAM: 32GB recommended (16GB minimum)
- Storage: 15GB free space
- Runtime: ~10-15 minutes

### Option 3: Interactive Notebook

Open `Chau_RoyaleClash.ipynb` in Google Colab or Jupyter for interactive exploration with a 800k battle sample (5% of full data).

## Analysis Features

### 📊 Full Dataset Analysis Script

The `full_dataset_analysis.py` script provides:

✅ Dataset structure and quality assessment
✅ Temporal coverage and battle frequency
✅ Comprehensive clan performance metrics
✅ Card meta and win rate analysis
✅ Elixir cost effectiveness
✅ Trophy range stratification
✅ Exported clan performance CSV

### 🎯 Key Metrics Calculated

**Per-Clan Metrics:**
- Total matches played
- Unique player count
- Win rate
- Trophy change (total, average, standard deviation)
- Crown statistics
- Average opponent strength
- Deck characteristics

**Per-Card Metrics:**
- Usage frequency across all battles
- Win rate when included in deck
- Performance by trophy bracket
- Synergy patterns (future work)

## Dataset Schema

### 74 Columns Total

**Battle Info (5):** Timestamp, arena, game mode, avg trophies, tournament tag

**Per-Player Data (26 columns × 2):**
- Identity: tag, clan tag, clan badge
- Performance: starting trophies, trophy change, crowns
- Deck: 8 cards with IDs and levels
- Stats: elixir average, card levels, composition breakdown

See [FULL_DATASET_ANALYSIS.md](FULL_DATASET_ANALYSIS.md) for complete column reference.

## Data Quality

### ✅ Strengths

- 100% complete battle core data (trophies, crowns, timestamps)
- All 16M+ battles have full deck information
- Well-structured and consistent format
- No duplicate battles detected

### ⚠️ Considerations

- ~4% of players have no clan affiliation
- Tower HP missing when 3-crown victory (~27% of matches)
- Tournament tag 100% null (ladder-only dataset)
- Single arena and game mode (no variety)

## Research Applications

This dataset is valuable for:

### 🎓 Academic Research

- Game theory and competitive balance
- Matchmaking algorithm fairness
- Player retention and engagement patterns
- Social dynamics in gaming communities

### 📈 Data Science Projects

- Win prediction machine learning models
- Deck recommendation systems
- Player behavior clustering
- Time series analysis of game meta

### 🎮 Game Design Insights

- Card balance assessment
- Progression system analysis
- Retention optimization
- Competitive ecosystem health

## Interesting Findings

### 🔥 Hot Takes

1. **Elixir cost doesn't matter** - Winners and losers have identical average elixir (3.84)
2. **Clans are struggling** - Nearly half only play one match and 98% of those lose
3. **Mid-ladder dominates** - 63% of all battles occur between 4,000-6,000 trophies
4. **3-crowns are common** - ~27% of matches end in complete destruction
5. **System is balanced** - Trophy gains perfectly offset trophy losses

### 📊 Statistical Curiosities

- **316,031** unique clans in just 800k battles (5% sample)
- **152,441** clans lost their only match and disappeared
- Average match has **crown difference of 0.84** (1.77 vs 0.93)
- Deck card levels vary by only **~1 level** between winner/loser

## Contributing

Contributions welcome! Areas for expansion:

- [ ] Card combination synergy analysis
- [ ] Player trajectory modeling
- [ ] Deck archetype classification
- [ ] Matchmaking fairness assessment
- [ ] Interactive visualizations
- [ ] Time-of-day performance patterns
- [ ] Clan lifecycle modeling

## Future Work

- Convert dataset to Parquet for faster loading
- Add card name mappings (currently only IDs)
- Integrate multiple time periods for meta evolution
- Build interactive dashboard (Streamlit/Plotly)
- Develop win prediction ML models

## Citation

If you use this dataset in research or projects, please cite:

```bibtex
@dataset{clashroyale_dec2020,
  title={Clash Royale Battle Dataset},
  author={Chau-Nguyen-Developer and Yamato-ship},
  year={2020},
  month={December},
  note={16.3M battles, 32.6M player-match records},
  url={https://github.com/Yamato-ship/HeHeHaHa_DataRoyale}
}
```

## License

Dataset sourced from Supercell's Clash Royale API. Analysis and code provided for educational and research purposes.

## Acknowledgments

- **Data Collection:** Original dataset compiled from Clash Royale API
- **Analysis:** Chau-Nguyen-Developer (primary analysis and notebook)
- **Repository:** Yamato-ship

## Contact

For questions, issues, or collaboration opportunities:
- Open an issue on GitHub
- Pull requests welcome!

---

**⚔️ Clash on, data enthusiasts! ⚔️**

*Last updated: November 2025*
