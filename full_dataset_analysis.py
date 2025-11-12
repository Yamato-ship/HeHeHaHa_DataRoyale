#!/usr/bin/env python3
"""
Full Dataset Analysis Script for Clash Royale Battle Data
This script analyzes the complete dataset without row limits
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")

def load_full_dataset(filepath="dataset.csv"):
    """Load the complete dataset"""
    print_section("Loading Full Dataset")
    print(f"Loading data from: {filepath}")
    print("This may take several minutes for large files...")

    # First, get the total number of rows
    print("\nCounting rows...")
    row_count = sum(1 for _ in open(filepath)) - 1  # Subtract header
    print(f"Total rows in dataset: {row_count:,}")

    # Load the full dataset
    print("\nLoading all data into memory...")
    start_time = datetime.now()
    data = pd.read_csv(filepath)
    load_time = (datetime.now() - start_time).total_seconds()

    print(f"✓ Loaded {len(data):,} rows in {load_time:.2f} seconds")
    print(f"✓ Memory usage: {data.memory_usage(deep=True).sum() / (1024**2):.2f} MB")

    return data

def analyze_dataset_structure(data):
    """Analyze basic dataset structure"""
    print_section("Dataset Structure")

    print(f"Shape: {data.shape[0]:,} rows × {data.shape[1]} columns")
    print(f"\nData types:")
    print(data.dtypes.value_counts())

    print(f"\nMissing values by column:")
    missing = data.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if len(missing) > 0:
        for col, count in missing.items():
            pct = (count / len(data)) * 100
            print(f"  {col}: {count:,} ({pct:.2f}%)")
    else:
        print("  No missing values!")

    return missing

def analyze_temporal_coverage(data):
    """Analyze time range of battles"""
    print_section("Temporal Coverage")

    data['battleTime'] = pd.to_datetime(data['battleTime'])

    print(f"First battle: {data['battleTime'].min()}")
    print(f"Last battle: {data['battleTime'].max()}")
    print(f"Time span: {(data['battleTime'].max() - data['battleTime'].min()).days} days")

    print(f"\nBattles per day:")
    battles_per_day = data.groupby(data['battleTime'].dt.date).size()
    print(f"  Average: {battles_per_day.mean():,.0f}")
    print(f"  Min: {battles_per_day.min():,}")
    print(f"  Max: {battles_per_day.max():,}")

    return battles_per_day

def analyze_clan_performance(data):
    """Comprehensive clan performance analysis"""
    print_section("Clan Performance Analysis")

    # Create per-player dataset
    print("Reshaping data to per-player format...")

    winners = pd.DataFrame({
        "playerTag": data["winner.tag"],
        "battleTime": data["battleTime"],
        "clanTag": data["winner.clan.tag"],
        "playerStartTrophies": data["winner.startingTrophies"],
        "opponentStartTrophies": data["loser.startingTrophies"],
        "trophyChange": data["winner.trophyChange"],
        "crownsGained": data["winner.crowns"],
        "crownsLost": data["loser.crowns"],
        "elixirAverage": data["winner.elixir.average"],
        "totalCardLevel": data["winner.totalcard.level"],
        "result": 1
    })

    losers = pd.DataFrame({
        "playerTag": data["loser.tag"],
        "battleTime": data["battleTime"],
        "clanTag": data["loser.clan.tag"],
        "playerStartTrophies": data["loser.startingTrophies"],
        "opponentStartTrophies": data["winner.startingTrophies"],
        "trophyChange": data["loser.trophyChange"],
        "crownsGained": data["loser.crowns"],
        "crownsLost": data["winner.crowns"],
        "elixirAverage": data["loser.elixir.average"],
        "totalCardLevel": data["loser.totalcard.level"],
        "result": 0
    })

    perPlayer = pd.concat([winners, losers], ignore_index=True)

    # Remove players without clans
    players_without_clans = perPlayer["clanTag"].isna().sum()
    print(f"Players without clans: {players_without_clans:,} ({players_without_clans/len(perPlayer)*100:.2f}%)")

    perPlayer = perPlayer.dropna(subset=["clanTag"])

    print(f"Total player-match records: {len(perPlayer):,}")
    print(f"Unique players: {perPlayer['playerTag'].nunique():,}")
    print(f"Unique clans: {perPlayer['clanTag'].nunique():,}")

    # Aggregate by clan
    print("\nCalculating clan-level metrics...")
    perClanAggregates = perPlayer.groupby("clanTag").agg(
        matches=("result", "size"),
        uniquePlayers=("playerTag", pd.Series.nunique),
        wins=("result", "sum"),
        winRate=("result", "mean"),
        totalCrownsGained=("crownsGained", "sum"),
        avgCrownsGained=("crownsGained", "mean"),
        totalTrophyChange=("trophyChange", "sum"),
        avgTrophyChange=("trophyChange", "mean"),
        avgOpponentTrophies=("opponentStartTrophies", "mean"),
        avgElixir=("elixirAverage", "mean"),
        avgCardLevel=("totalCardLevel", "mean")
    ).reset_index()

    # Calculate trophy change standard deviation
    perClanAggregates["trophyChangeSTD"] = perClanAggregates["clanTag"].map(
        perPlayer.groupby("clanTag")["trophyChange"].std()
    )

    print(f"\nClan Statistics:")
    print(f"  Total clans: {len(perClanAggregates):,}")
    print(f"  Avg matches per clan: {perClanAggregates['matches'].mean():.2f}")
    print(f"  Median matches per clan: {perClanAggregates['matches'].median():.0f}")
    print(f"  Avg unique players per clan: {perClanAggregates['uniquePlayers'].mean():.2f}")

    # Match distribution
    print(f"\nMatch Distribution:")
    for threshold in [1, 2, 5, 10, 50, 100, 500]:
        count = (perClanAggregates['matches'] >= threshold).sum()
        pct = count / len(perClanAggregates) * 100
        print(f"  Clans with ≥{threshold:>3} matches: {count:>6,} ({pct:>5.2f}%)")

    # Single-match clan analysis
    single_match_clans = perClanAggregates[perClanAggregates['matches'] == 1]
    print(f"\nSingle-Match Clan Analysis:")
    print(f"  Count: {len(single_match_clans):,} ({len(single_match_clans)/len(perClanAggregates)*100:.2f}%)")
    print(f"  Win rate: {single_match_clans['winRate'].mean()*100:.2f}%")
    print(f"  Avg trophy change: {single_match_clans['avgTrophyChange'].mean():.2f}")

    # Top performing clans (min 100 matches)
    active_clans = perClanAggregates[perClanAggregates['matches'] >= 100].copy()
    if len(active_clans) > 0:
        print(f"\nTop 10 Clans by Win Rate (min 100 matches):")
        top_clans = active_clans.nlargest(10, 'winRate')
        for idx, row in top_clans.iterrows():
            print(f"  {row['clanTag']}: {row['winRate']*100:.2f}% WR, {row['matches']:,} matches, {row['avgTrophyChange']:.2f} avg trophy Δ")

    return perPlayer, perClanAggregates

def analyze_card_meta(data):
    """Analyze card usage and win rates"""
    print_section("Card Meta Analysis")

    # Collect all card IDs from winners and losers
    print("Analyzing card usage patterns...")

    winner_cards = []
    loser_cards = []

    for i in range(1, 9):
        winner_cards.append(data[f'winner.card{i}.id'])
        loser_cards.append(data[f'loser.card{i}.id'])

    # Winner card stats
    winner_card_series = pd.concat(winner_cards, ignore_index=True)
    winner_card_counts = winner_card_series.value_counts()

    # Loser card stats
    loser_card_series = pd.concat(loser_cards, ignore_index=True)
    loser_card_counts = loser_card_series.value_counts()

    # Total usage
    total_card_usage = winner_card_counts.add(loser_card_counts, fill_value=0)

    print(f"Unique cards in dataset: {len(total_card_usage)}")
    print(f"\nTop 20 Most Used Cards:")
    for idx, (card_id, count) in enumerate(total_card_usage.head(20).items(), 1):
        usage_rate = count / (len(data) * 16) * 100  # 16 total card slots per match
        win_count = winner_card_counts.get(card_id, 0)
        loss_count = loser_card_counts.get(card_id, 0)
        win_rate = win_count / (win_count + loss_count) * 100 if (win_count + loss_count) > 0 else 0
        print(f"  {idx:>2}. Card {card_id}: {count:>8,} uses ({usage_rate:>5.2f}%), WR: {win_rate:.2f}%")

    return total_card_usage, winner_card_counts, loser_card_counts

def analyze_elixir_trends(data):
    """Analyze elixir cost trends"""
    print_section("Elixir Cost Analysis")

    print("Winner Elixir Average:")
    print(f"  Mean: {data['winner.elixir.average'].mean():.3f}")
    print(f"  Median: {data['winner.elixir.average'].median():.3f}")
    print(f"  Std Dev: {data['winner.elixir.average'].std():.3f}")

    print("\nLoser Elixir Average:")
    print(f"  Mean: {data['loser.elixir.average'].mean():.3f}")
    print(f"  Median: {data['loser.elixir.average'].median():.3f}")
    print(f"  Std Dev: {data['loser.elixir.average'].std():.3f}")

    elixir_diff = data['winner.elixir.average'] - data['loser.elixir.average']
    print(f"\nElixir Difference (Winner - Loser):")
    print(f"  Mean: {elixir_diff.mean():.3f}")
    print(f"  Median: {elixir_diff.median():.3f}")

    # Correlation with winning
    print(f"\nDoes higher/lower elixir correlate with winning?")
    higher_elixir_wins = (data['winner.elixir.average'] > data['loser.elixir.average']).sum()
    print(f"  Winner had higher elixir: {higher_elixir_wins:,} ({higher_elixir_wins/len(data)*100:.2f}%)")

def analyze_trophy_ranges(data):
    """Analyze performance across trophy ranges"""
    print_section("Trophy Range Analysis")

    data['trophy_bracket'] = pd.cut(
        data['average.startingTrophies'],
        bins=[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000],
        labels=['0-1k', '1-2k', '2-3k', '3-4k', '4-5k', '5-6k', '6-7k', '7-8k', '8k+']
    )

    trophy_stats = data.groupby('trophy_bracket', observed=True).agg({
        'average.startingTrophies': 'count',
        'winner.trophyChange': 'mean',
        'loser.trophyChange': 'mean',
        'winner.elixir.average': 'mean',
        'loser.elixir.average': 'mean',
        'winner.totalcard.level': 'mean',
        'loser.totalcard.level': 'mean'
    }).round(2)

    trophy_stats.columns = ['Matches', 'Avg Win Trophy Δ', 'Avg Loss Trophy Δ',
                            'Win Elixir', 'Loss Elixir', 'Win Card Lvl', 'Loss Card Lvl']

    print(trophy_stats.to_string())

def main():
    """Main analysis pipeline"""
    try:
        # Load data
        data = load_full_dataset()

        # Run analyses
        analyze_dataset_structure(data)
        analyze_temporal_coverage(data)
        perPlayer, perClanAggregates = analyze_clan_performance(data)
        analyze_card_meta(data)
        analyze_elixir_trends(data)
        analyze_trophy_ranges(data)

        # Save aggregated data
        print_section("Saving Results")
        perClanAggregates.to_csv('clan_performance_full.csv', index=False)
        print("✓ Saved clan performance data to 'clan_performance_full.csv'")

        print_section("Analysis Complete")
        print("Full dataset analysis finished successfully!")

    except FileNotFoundError:
        print("ERROR: dataset.csv not found!")
        print("Please ensure the dataset is downloaded to the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
