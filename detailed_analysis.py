#!/usr/bin/env python3
"""
Detailed Dataset Analysis
Analyzes clan membership, card usage, crown patterns, and temporal patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")

def analyze_clan_membership(data):
    """Detailed analysis of players with/without clans"""
    print_header("CLAN MEMBERSHIP ANALYSIS")

    total_battles = len(data)
    total_player_records = total_battles * 2

    # Count players with and without clans
    winners_with_clan = data['winner.clan.tag'].notna().sum()
    winners_without_clan = data['winner.clan.tag'].isna().sum()

    losers_with_clan = data['loser.clan.tag'].notna().sum()
    losers_without_clan = data['loser.clan.tag'].isna().sum()

    total_with_clan = winners_with_clan + losers_with_clan
    total_without_clan = winners_without_clan + losers_without_clan

    print(f"Total Battles: {total_battles:,}")
    print(f"Total Player-Match Records: {total_player_records:,}")
    print()

    print("="*80)
    print("OVERALL CLAN MEMBERSHIP")
    print("="*80)
    print(f"Players WITH clan:    {total_with_clan:>10,} ({total_with_clan/total_player_records*100:>6.2f}%)")
    print(f"Players WITHOUT clan: {total_without_clan:>10,} ({total_without_clan/total_player_records*100:>6.2f}%)")
    print()

    print("="*80)
    print("BREAKDOWN BY WIN/LOSS")
    print("="*80)
    print(f"Winners WITH clan:    {winners_with_clan:>10,} ({winners_with_clan/total_battles*100:>6.2f}%)")
    print(f"Winners WITHOUT clan: {winners_without_clan:>10,} ({winners_without_clan/total_battles*100:>6.2f}%)")
    print()
    print(f"Losers WITH clan:     {losers_with_clan:>10,} ({losers_with_clan/total_battles*100:>6.2f}%)")
    print(f"Losers WITHOUT clan:  {losers_without_clan:>10,} ({losers_without_clan/total_battles*100:>6.2f}%)")
    print()

    # Calculate win rates
    print("="*80)
    print("WIN RATE BY CLAN MEMBERSHIP")
    print("="*80)

    # For players with clans
    clan_player_wins = winners_with_clan
    clan_player_total = total_with_clan
    clan_win_rate = clan_player_wins / clan_player_total * 100

    # For players without clans
    no_clan_player_wins = winners_without_clan
    no_clan_player_total = total_without_clan
    no_clan_win_rate = no_clan_player_wins / no_clan_player_total * 100

    print(f"Players WITH clan win rate:    {clan_win_rate:.2f}%")
    print(f"Players WITHOUT clan win rate: {no_clan_win_rate:.2f}%")
    print()

    # Key insights
    print("="*80)
    print("KEY INSIGHTS")
    print("="*80)

    if clan_win_rate > no_clan_win_rate:
        diff = clan_win_rate - no_clan_win_rate
        print(f"✓ Players WITH clans win {diff:.2f}% MORE often than players without clans")
    else:
        diff = no_clan_win_rate - clan_win_rate
        print(f"✓ Players WITHOUT clans win {diff:.2f}% MORE often than players with clans")

    print(f"✓ Winners are {winners_without_clan/losers_without_clan:.2f}x LESS likely to be clanless than losers")
    print(f"✓ Only {winners_without_clan/total_battles*100:.2f}% of winners have no clan")
    print(f"✓ But {losers_without_clan/total_battles*100:.2f}% of losers have no clan")
    print()

def analyze_top_cards(data):
    """Analyze top 5 most common cards for winners and losers"""
    print_header("TOP 5 MOST COMMON CARDS")

    # Collect all winner cards
    winner_cards = []
    for i in range(1, 9):
        winner_cards.extend(data[f'winner.card{i}.id'].tolist())

    # Collect all loser cards
    loser_cards = []
    for i in range(1, 9):
        loser_cards.extend(data[f'loser.card{i}.id'].tolist())

    # Count occurrences
    winner_card_counts = Counter(winner_cards)
    loser_card_counts = Counter(loser_cards)

    # Get top 5
    top_winner_cards = winner_card_counts.most_common(5)
    top_loser_cards = loser_card_counts.most_common(5)

    total_winner_card_slots = len(data) * 8
    total_loser_card_slots = len(data) * 8

    print("="*80)
    print("TOP 5 CARDS IN WINNING DECKS")
    print("="*80)
    for idx, (card_id, count) in enumerate(top_winner_cards, 1):
        usage_rate = count / total_winner_card_slots * 100
        appearances = count / len(data) * 100
        print(f"{idx}. Card ID {card_id}:")
        print(f"   Used in {count:,} card slots ({usage_rate:.2f}% of all winner card slots)")
        print(f"   Appeared in {count:,} winning decks ({appearances:.1f}% of winners)")
        print()

    print("="*80)
    print("TOP 5 CARDS IN LOSING DECKS")
    print("="*80)
    for idx, (card_id, count) in enumerate(top_loser_cards, 1):
        usage_rate = count / total_loser_card_slots * 100
        appearances = count / len(data) * 100
        print(f"{idx}. Card ID {card_id}:")
        print(f"   Used in {count:,} card slots ({usage_rate:.2f}% of all loser card slots)")
        print(f"   Appeared in {count:,} losing decks ({appearances:.1f}% of losers)")
        print()

    # Compare overlap
    print("="*80)
    print("CARD USAGE COMPARISON")
    print("="*80)

    winner_card_set = set([card_id for card_id, _ in top_winner_cards])
    loser_card_set = set([card_id for card_id, _ in top_loser_cards])
    overlap = winner_card_set & loser_card_set

    print(f"Cards appearing in both top 5 lists: {len(overlap)}")
    if overlap:
        print(f"Overlapping cards: {overlap}")
    print()

    # Calculate win rates for top cards
    print("="*80)
    print("WIN RATES OF TOP 5 WINNER CARDS")
    print("="*80)
    for card_id, winner_count in top_winner_cards:
        loser_count = loser_card_counts.get(card_id, 0)
        total_uses = winner_count + loser_count
        win_rate = winner_count / total_uses * 100 if total_uses > 0 else 0
        print(f"Card ID {card_id}: {win_rate:.2f}% win rate ({winner_count:,} wins / {total_uses:,} total uses)")
    print()

def analyze_crown_patterns(data):
    """Analyze crown patterns for wins and losses"""
    print_header("CROWN PATTERN ANALYSIS")

    total_battles = len(data)

    # Winners by crown count
    print("="*80)
    print("WINNER CROWN DISTRIBUTION")
    print("="*80)
    for crowns in [1, 2, 3]:
        count = (data['winner.crowns'] == crowns).sum()
        pct = count / total_battles * 100
        print(f"{crowns}-Crown Wins: {count:>10,} ({pct:>6.2f}%)")

    avg_winner_crowns = data['winner.crowns'].mean()
    print(f"\nAverage winner crowns: {avg_winner_crowns:.2f}")
    print()

    # Losers by crown count
    print("="*80)
    print("LOSER CROWN DISTRIBUTION")
    print("="*80)
    for crowns in [0, 1, 2]:
        count = (data['loser.crowns'] == crowns).sum()
        pct = count / total_battles * 100
        print(f"{crowns}-Crown Losses: {count:>10,} ({pct:>6.2f}%)")

    avg_loser_crowns = data['loser.crowns'].mean()
    print(f"\nAverage loser crowns: {avg_loser_crowns:.2f}")
    print()

    # Specific patterns requested
    print("="*80)
    print("SPECIFIC PATTERNS")
    print("="*80)

    wins_with_2_crowns = (data['winner.crowns'] == 2).sum()
    wins_with_2_crowns_pct = wins_with_2_crowns / total_battles * 100

    losses_with_0_crowns = (data['loser.crowns'] == 0).sum()
    losses_with_0_crowns_pct = losses_with_0_crowns / total_battles * 100

    print(f"Players who win with EXACTLY 2 crowns: {wins_with_2_crowns:,} ({wins_with_2_crowns_pct:.2f}% of all battles)")
    print(f"Players who lose with EXACTLY 0 crowns: {losses_with_0_crowns:,} ({losses_with_0_crowns_pct:.2f}% of all battles)")
    print()

    # Crown difference analysis
    print("="*80)
    print("CROWN DIFFERENCE ANALYSIS")
    print("="*80)

    data['crown_difference'] = data['winner.crowns'] - data['loser.crowns']

    for diff in sorted(data['crown_difference'].unique()):
        count = (data['crown_difference'] == diff).sum()
        pct = count / total_battles * 100
        print(f"Crown difference of {int(diff)}: {count:>10,} ({pct:>6.2f}%)")

    avg_crown_diff = data['crown_difference'].mean()
    print(f"\nAverage crown difference: {avg_crown_diff:.2f}")
    print()

    # Most common match outcomes
    print("="*80)
    print("MOST COMMON MATCH OUTCOMES (Winner-Loser Crown Scores)")
    print("="*80)

    outcome_counts = data.groupby(['winner.crowns', 'loser.crowns']).size().sort_values(ascending=False)

    for idx, ((w_crowns, l_crowns), count) in enumerate(outcome_counts.head(10).items(), 1):
        pct = count / total_battles * 100
        print(f"{idx}. {int(w_crowns)}-{int(l_crowns)}: {count:>10,} battles ({pct:>6.2f}%)")
    print()

def analyze_temporal_patterns(data):
    """Analyze patterns by day and time"""
    print_header("TEMPORAL PATTERN ANALYSIS")

    # Convert to datetime
    data['battleTime'] = pd.to_datetime(data['battleTime'])
    data['date'] = data['battleTime'].dt.date
    data['hour'] = data['battleTime'].dt.hour
    data['day_of_week'] = data['battleTime'].dt.day_name()
    data['day_of_week_num'] = data['battleTime'].dt.dayofweek

    print("="*80)
    print("DATASET TIME RANGE")
    print("="*80)
    print(f"First battle: {data['battleTime'].min()}")
    print(f"Last battle:  {data['battleTime'].max()}")
    print(f"Duration: {(data['battleTime'].max() - data['battleTime'].min()).days} days")
    print()

    # Battles per day
    print("="*80)
    print("BATTLES PER DAY")
    print("="*80)

    battles_per_day = data.groupby('date').size().sort_index()

    for date, count in battles_per_day.items():
        day_name = pd.Timestamp(date).day_name()
        print(f"{date} ({day_name}): {count:>8,} battles")

    print(f"\nAverage battles per day: {battles_per_day.mean():,.0f}")
    print(f"Peak day: {battles_per_day.idxmax()} with {battles_per_day.max():,} battles")
    print(f"Slowest day: {battles_per_day.idxmin()} with {battles_per_day.min():,} battles")
    print()

    # Day of week patterns
    print("="*80)
    print("BATTLES BY DAY OF WEEK")
    print("="*80)

    battles_by_dow = data.groupby('day_of_week_num').agg({
        'day_of_week': 'first',
        'winner.tag': 'count'
    }).rename(columns={'winner.tag': 'battles'})

    battles_by_dow = battles_by_dow.sort_index()

    for idx, row in battles_by_dow.iterrows():
        day_name = row['day_of_week']
        count = row['battles']
        pct = count / len(data) * 100
        print(f"{day_name:>9}: {count:>8,} battles ({pct:>5.2f}%)")
    print()

    # Hourly patterns
    print("="*80)
    print("BATTLES BY HOUR OF DAY (UTC)")
    print("="*80)

    battles_by_hour = data.groupby('hour').size().sort_index()

    for hour, count in battles_by_hour.items():
        pct = count / len(data) * 100
        bar = '█' * int(pct * 2)
        print(f"{hour:>2}:00 - {count:>7,} battles ({pct:>5.2f}%) {bar}")

    peak_hour = battles_by_hour.idxmax()
    print(f"\nPeak hour: {peak_hour}:00 UTC with {battles_by_hour.max():,} battles")
    print()

    # Trophy change patterns by time
    print("="*80)
    print("AVERAGE TROPHY CHANGE BY DAY")
    print("="*80)

    trophy_by_day = data.groupby('date').agg({
        'winner.trophyChange': 'mean',
        'loser.trophyChange': 'mean'
    })

    for date, row in trophy_by_day.iterrows():
        day_name = pd.Timestamp(date).day_name()
        print(f"{date} ({day_name}): Winner Δ{row['winner.trophyChange']:>6.2f}, Loser Δ{row['loser.trophyChange']:>7.2f}")
    print()

def main():
    """Main analysis function"""
    print("\n" + "█"*80)
    print(" "*25 + "DETAILED DATASET ANALYSIS")
    print("█"*80)

    # Load data
    print("\nLoading dataset...")
    try:
        # Try to load full dataset first
        data = pd.read_csv("dataset.csv", nrows=800_000)
        print(f"✓ Loaded {len(data):,} battles (800k sample)")
    except FileNotFoundError:
        print("ERROR: dataset.csv not found!")
        print("Please download the dataset first or run this from Google Colab.")
        return

    # Run all analyses
    analyze_clan_membership(data)
    analyze_top_cards(data)
    analyze_crown_patterns(data)
    analyze_temporal_patterns(data)

    print("\n" + "="*80)
    print(" ANALYSIS COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
