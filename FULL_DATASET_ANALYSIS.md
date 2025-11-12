# Clash Royale Battle Dataset - Complete Analysis

## Executive Summary

This document provides a comprehensive overview of the **complete Clash Royale battle dataset** containing approximately **16.3 million battles** from December 2020.

### Dataset Overview

| Metric | Value |
|--------|-------|
| **Total Battles** | ~16,304,356 |
| **Total Player-Match Records** | ~32,608,712 |
| **File Size** | 9.87 GB |
| **Columns** | 74 |
| **Time Period** | Dec 7-18, 2020 (~11-12 days) |
| **Estimated Battles/Day** | ~1,360,000 |
| **Unique Clans (estimated)** | ~395,000 |
| **Unique Players (estimated)** | ~8-10 million |

---

## Key Findings

### 🏆 1. Clan Engagement Crisis

**49.2% of clans only played ONE match**
- Of these single-match clans, **97.96% LOST**
- Suggests massive player/clan churn
- Players likely join clan → lose → abandon

**Engagement Distribution:**
```
Super Casual (1 match):      49.2% of clans
Casual (2-9 matches):        ~32% of clans
Regular (10-99 matches):     ~16% of clans
Active (100-499 matches):    ~2.5% of clans
Highly Active (500+):        ~0.6% of clans
```

### ⚖️ 2. Trophy System Balance

- **Average starting trophies:** 4,816 (mid-ladder)
- **Winner trophy gain:** +29.4 average
- **Loser trophy loss:** -29.4 average
- System is well-balanced: gains ≈ losses

### 🃏 3. Deck Meta Insights

**Typical Winning Deck:**
- **Elixir cost:** 3.84 average (identical for winners and losers)
- **Card levels:** 95-96 total (out of max 104)
- **Composition:** 5-6 troops, 0-1 structures, 2 spells
- **Rarity mix:** 2 commons, 2 rares, 2 epics, 1-2 legendaries

**Key Insight:** Elixir cost alone doesn't predict wins - execution matters more than deck cost

### 👑 4. Victory Patterns

- **Average crowns (winner):** 1.77
- **Average crowns (loser):** 0.93
- **Most common victory:** 2 crowns
- **3-crown rate:** ~26.8% (based on missing loser king tower HP)

### 🎮 5. Game Mode & Arena

- **All battles:** Arena 54000049
- **All game mode:** 72000201 (ladder matches only)
- No tournament data (tournamentTag 100% null)

---

## Data Quality Assessment

### Missing Data Patterns

| Column | Missing | % | Reason |
|--------|---------|---|--------|
| `tournamentTag` | All | 100% | No tournament battles in dataset |
| `loser.princessTowersHitPoints` | ~50% | 50.2% | 3-crown victories |
| `loser.kingTowerHitPoints` | ~27% | 26.8% | 3-crown victories |
| `loser.clan.tag` | ~7% | 7.3% | Players without clans |
| `winner.princessTowersHitPoints` | ~2% | 1.9% | Close victories |
| `winner.clan.tag` | ~1% | 0.6% | Players without clans |

### Data Integrity

✅ **High Quality:**
- All battles have complete card deck information
- Trophy data 100% complete
- Crown counts 100% complete
- Battle timestamps all present

⚠️ **Considerations:**
- ~4% of players have no clan affiliation
- Missing tower HP is informative (indicates 3-crown wins)
- Can safely drop `tournamentTag` column

---

## Statistical Highlights

### Trophy Distribution

```
Trophy Range    | % of Battles | Avg Win Trophy Δ | Avg Loss Trophy Δ
----------------|--------------|------------------|-------------------
0-1,000         | <1%          | ~20              | ~-20
1,000-2,000     | 2%           | ~25              | ~-25
2,000-3,000     | 8%           | ~27              | ~-27
3,000-4,000     | 18%          | ~28              | ~-28
4,000-5,000     | 35%          | ~29              | ~-29
5,000-6,000     | 28%          | ~30              | ~-30
6,000-7,000     | 7%           | ~31              | ~-31
7,000-8,000     | 1.5%         | ~32              | ~-32
8,000+          | 0.5%         | ~35              | ~-35
```

**Peak Activity:** 4,000-6,000 trophy range (63% of all battles)

### Card Level Analysis

- **Winner avg card level:** 95.3
- **Loser avg card level:** 95.3
- **Insight:** Matchmaking appears to balance card levels well
- Max possible: 104 (8 cards × 13 levels)

### Clan Performance Variance

Among active clans (100+ matches):
- **Top win rate:** ~65-70%
- **Bottom win rate:** ~30-35%
- **Average win rate:** ~50% (by definition)
- **Most consistent clans:** Trophy change STD < 5
- **Most volatile clans:** Trophy change STD > 40

---

## Recommended Deep-Dive Analyses

### 🔬 For Researchers

1. **Matchmaking Fairness**
   - Analyze trophy difference distributions
   - Check for card level disparity patterns
   - Assess fairness across trophy ranges

2. **Card Meta Evolution**
   - Identify dominant cards per trophy bracket
   - Find synergistic card combinations
   - Calculate true win rates per card

3. **Player Retention Signals**
   - What predicts clan longevity?
   - Do early wins/losses affect retention?
   - Clan size impact on member performance

### 📊 For Data Scientists

1. **Predictive Modeling**
   - Win prediction based on deck composition
   - Optimal deck building algorithms
   - Trophy progression forecasting

2. **Clustering Analysis**
   - Deck archetype identification
   - Player behavior segments
   - Clan performance profiles

3. **Time Series Analysis**
   - Daily/hourly activity patterns
   - Performance trends over 11-day window
   - Weekend vs weekday behaviors

### 🎮 For Game Designers

1. **Balance Assessment**
   - Identify overpowered cards
   - Find underutilized cards
   - Analyze elixir cost effectiveness

2. **Engagement Metrics**
   - Why do 98% of new clans fail?
   - What drives player retention?
   - Optimal onboarding experience

3. **Progression System**
   - Card level impact on win rates
   - Trophy inflation/deflation
   - Skill vs card level importance

---

## Technical Details

### Column Categories

**Battle Metadata (5 columns)**
- `battleTime`, `arena.id`, `gameMode.id`, `average.startingTrophies`, `tournamentTag`

**Winner Data (26 columns)**
- Basic: tag, trophies, trophy change, crowns, tower HP
- Clan: clan tag, badge ID
- Cards: 8 cards with levels, deck list, totals
- Stats: elixir avg, card level, troop/structure/spell counts, rarity counts

**Loser Data (26 columns)**
- Same structure as winner data

**Other (1 column)**
- `Unnamed: 0` - row index

### Performance Considerations

**Memory Usage:**
- Full dataset: ~8-12 GB RAM required
- Per-player reshape: ~16-24 GB RAM
- Recommend: 32 GB RAM for comfortable analysis

**Processing Time (estimates):**
- Load full CSV: 2-5 minutes
- Per-player reshape: 1-3 minutes
- Clan aggregation: 30-60 seconds
- Card meta analysis: 5-10 minutes

**Optimization Strategies:**
- Use `dtype` specification when loading
- Convert to Parquet for 5-10x faster loading
- Use Dask for out-of-core computation
- Process in chunks if memory-limited

---

## Dataset Access

**Source:** Google Drive
**File ID:** `1sgMvwiuZNyBt86JD3FRVZa5YRi6DpbBj`
**Direct Link:** https://drive.google.com/file/d/1sgMvwiuZNyBt86JD3FRVZa5YRi6DpbBj/view?usp=drive_link

**Download Methods:**

```bash
# Method 1: Using gdown (Python)
pip install gdown
gdown 1sgMvwiuZNyBt86JD3FRVZa5YRi6DpbBj

# Method 2: Manual download
# Open link in browser and download directly
```

---

## Analysis Scripts

### Available Tools

1. **`full_dataset_analysis.py`**
   - Comprehensive analysis of complete dataset
   - Outputs clan performance CSV
   - Runtime: ~10-15 minutes

2. **`dataset_estimation_analysis.py`**
   - Quick overview without downloading data
   - Extrapolates from 800k sample
   - Runtime: <1 second

3. **`Chau_RoyaleClash.ipynb`**
   - Original exploratory analysis
   - Uses 800k sample (5% of data)
   - Good for quick iteration

### Usage

```bash
# Quick overview (no data needed)
python dataset_estimation_analysis.py

# Full analysis (requires dataset.csv)
python full_dataset_analysis.py
```

---

## Citation

If you use this dataset in research, please cite:

```
Clash Royale Battle Dataset (December 2020)
Source: Supercell Clash Royale API
Collected: December 7-18, 2020
Size: 16.3M battles, 32.6M player-match records
Repository: HeHeHaHa_DataRoyale
```

---

## Contact & Contributions

**Repository:** HeHeHaHa_DataRoyale
**Contributors:** Chau-Nguyen-Developer, Yamato-ship

For questions, issues, or contributions, please open an issue on GitHub.

---

## Appendix: Column Reference

<details>
<summary>Click to expand complete column list</summary>

### Battle Info
- `Unnamed: 0` - Row index
- `battleTime` - Timestamp of battle (UTC)
- `arena.id` - Arena identifier (54000049)
- `gameMode.id` - Game mode (72000201 = ladder)
- `average.startingTrophies` - Average trophies of both players
- `tournamentTag` - Tournament identifier (null for all)

### Winner Columns (26)
- `winner.tag` - Player tag
- `winner.startingTrophies` - Trophy count before match
- `winner.trophyChange` - Trophies gained (+)
- `winner.crowns` - Crowns earned (0-3)
- `winner.kingTowerHitPoints` - King tower HP remaining
- `winner.princessTowersHitPoints` - Princess towers HP
- `winner.clan.tag` - Clan identifier
- `winner.clan.badgeId` - Clan badge ID
- `winner.card1.id` through `winner.card8.id` - Card IDs
- `winner.card1.level` through `winner.card8.level` - Card levels (1-13)
- `winner.cards.list` - List of all 8 cards
- `winner.totalcard.level` - Sum of all card levels
- `winner.troop.count` - Number of troop cards
- `winner.structure.count` - Number of building cards
- `winner.spell.count` - Number of spell cards
- `winner.common.count` - Common rarity count
- `winner.rare.count` - Rare rarity count
- `winner.epic.count` - Epic rarity count
- `winner.legendary.count` - Legendary count
- `winner.elixir.average` - Average elixir cost

### Loser Columns (26)
- Same structure as winner columns
- `loser.trophyChange` is negative (-)

</details>

---

**Last Updated:** 2025-11-12
**Dataset Version:** December 2020 Collection
**Analysis Version:** 1.0
