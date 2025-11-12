#!/usr/bin/env python3
"""
Full Dataset Estimation Analysis
Estimates full dataset characteristics based on the 800k sample from the notebook
"""

import pandas as pd
import numpy as np

def estimate_full_dataset_size():
    """Estimate full dataset size based on known information"""
    print("="*80)
    print(" FULL DATASET SIZE ESTIMATION")
    print("="*80)
    print()

    # Known facts from notebook
    file_size_gb = 9.87
    sample_rows = 800_000
    num_columns = 74

    print(f"Known Information:")
    print(f"  File size: {file_size_gb:.2f} GB")
    print(f"  Sample loaded: {sample_rows:,} rows")
    print(f"  Number of columns: {num_columns}")
    print()

    # Estimate total rows
    # Average bytes per row in sample
    # CSV overhead estimation: ~400-500 bytes per row for 74 columns
    estimated_bytes_per_row = 650  # Conservative estimate

    total_bytes = file_size_gb * 1024**3
    estimated_total_rows = int(total_bytes / estimated_bytes_per_row)

    print(f"Estimated Total Dataset:")
    print(f"  Total rows: ~{estimated_total_rows:,} battles")
    print(f"  Player-match records: ~{estimated_total_rows * 2:,}")
    print(f"  Sample represents: ~{sample_rows/estimated_total_rows*100:.1f}% of full data")
    print()

    return estimated_total_rows

def extrapolate_clan_statistics():
    """Extrapolate clan statistics from the sample"""
    print("="*80)
    print(" EXTRAPOLATED CLAN STATISTICS (from 800k sample)")
    print("="*80)
    print()

    # Known statistics from the notebook analysis
    sample_size = 800_000
    unique_clans_in_sample = 316_031
    single_match_clans = 155_616
    players_without_clans = 63_656

    print(f"Sample Analysis (800k battles):")
    print(f"  Unique clans: {unique_clans_in_sample:,}")
    print(f"  Single-match clans: {single_match_clans:,} ({single_match_clans/unique_clans_in_sample*100:.2f}%)")
    print(f"  Single-match clans that lost: {152_441:,} ({152_441/single_match_clans*100:.2f}%)")
    print(f"  Players without clans: {players_without_clans:,} ({players_without_clans/(sample_size*2)*100:.2f}%)")
    print()

    # Extrapolations for full dataset (~15.2M battles based on file size)
    estimated_total_battles = 15_200_000

    # New clans likely follow diminishing returns
    # Many clans in sample only appear once, suggesting we're capturing most active clans
    # Estimate: ~20-30% more unique clans in full dataset
    estimated_total_clans = int(unique_clans_in_sample * 1.25)

    # Single-match clans will likely increase linearly with data
    estimated_single_match_clans = int(single_match_clans * (estimated_total_battles / sample_size))

    print(f"Estimated Full Dataset (~15.2M battles):")
    print(f"  Total unique clans: ~{estimated_total_clans:,}")
    print(f"  Single-match clans: ~{estimated_single_match_clans:,}")
    print(f"  Active clans (>100 matches): likely similar to sample due to time window")
    print()

    return estimated_total_battles, estimated_total_clans

def analyze_data_quality_insights():
    """Analyze data quality observations"""
    print("="*80)
    print(" DATA QUALITY OBSERVATIONS")
    print("="*80)
    print()

    print("Missing Data Patterns:")
    print("  • winner.princessTowersHitPoints: 15,273 missing (1.9%)")
    print("  • winner.clan.tag: 5,103 missing (0.6%)")
    print("  • loser.clan.tag: 58,553 missing (7.3%)")
    print("  • loser.kingTowerHitPoints: 214,116 missing (26.8%)")
    print("  • loser.princessTowersHitPoints: 401,579 missing (50.2%)")
    print("  • tournamentTag: 800,000 missing (100% - can be dropped)")
    print()

    print("Key Observations:")
    print("  • All battles are from game mode 72000201 (likely ladder matches)")
    print("  • All battles from arena 54000049")
    print("  • Winners much more likely to have clan affiliation (94%) vs losers (93%)")
    print("  • Loser tower HP often missing (3-crown victories)")
    print()

def analyze_temporal_insights():
    """Analyze temporal patterns from notebook"""
    print("="*80)
    print(" TEMPORAL ANALYSIS")
    print("="*80)
    print()

    print("Time Range (from sample):")
    print("  Start: 2020-12-07 07:00:00+00:00")
    print("  Likely duration: ~11-12 days (based on 800k sample)")
    print("  Estimated battles/day: ~65,000-70,000")
    print()

    print("Full Dataset Estimate:")
    print("  If 15.2M battles: likely covers similar time period")
    print("  Represents: High-activity period in December 2020")
    print()

def analyze_competitive_insights():
    """Analyze competitive insights from the data"""
    print("="*80)
    print(" COMPETITIVE META INSIGHTS")
    print("="*80)
    print()

    print("Trophy Dynamics:")
    print("  • Average starting trophies: 4,816")
    print("  • Most battles in 4,500-5,200 range (mid-ladder)")
    print("  • Winner average trophy change: +29.4")
    print("  • System appears balanced (winners gain ~= losers lose)")
    print()

    print("Deck Composition Patterns:")
    print("  • Average elixir cost: 3.84 (both winners and losers)")
    print("  • Average deck level: ~95-96 (out of max 104)")
    print("  • Typical composition: 5-6 troops, 0-1 structures, 2 spells")
    print("  • Card rarity: ~2 commons, 2 rares, 2 epics, 1-2 legendaries")
    print()

    print("Win Patterns:")
    print("  • Average crown difference: 1.77 (winner) vs 0.93 (loser)")
    print("  • Most common victory: 2 crowns")
    print("  • 3-crown victories common (explains missing loser tower HP)")
    print()

def clan_engagement_insights():
    """Insights about clan engagement"""
    print("="*80)
    print(" CLAN ENGAGEMENT INSIGHTS")
    print("="*80)
    print()

    print("Engagement Tiers (from sample):")
    print("  1. Super Casual (1 match):    155,616 clans (49.2%)")
    print("  2. Casual (2-9 matches):      likely ~100,000 clans (32%)")
    print("  3. Regular (10-99 matches):   likely ~50,000 clans (16%)")
    print("  4. Active (100-499 matches):  likely ~8,000 clans (2.5%)")
    print("  5. Highly Active (500+ matches): likely ~2,000 clans (0.6%)")
    print()

    print("Key Finding: Clan Churn")
    print("  • 49% of clans only appear in ONE match")
    print("  • Of those, 98% LOST their only match")
    print("  • Suggests: Players join/create clans, lose, abandon clan")
    print("  • Indicates high player/clan churn in the game")
    print()

def research_questions():
    """Suggest research questions for full dataset"""
    print("="*80)
    print(" RECOMMENDED ANALYSES FOR FULL DATASET")
    print("="*80)
    print()

    questions = [
        "1. Card Meta Evolution",
        "   → Which cards have highest win rates at each trophy level?",
        "   → What are the most effective deck archetypes?",
        "   → How does card level advantage correlate with wins?",
        "",
        "2. Clan Lifecycle Analysis",
        "   → How do clans grow/shrink over the 11-day period?",
        "   → What separates successful clans from failed ones?",
        "   → Do clan members influence each other's performance?",
        "",
        "3. Player Skill vs Card Levels",
        "   → How much does card level disparity affect outcomes?",
        "   → Can skilled players overcome level disadvantages?",
        "   → What's the trophy range where levels matter most?",
        "",
        "4. Matchmaking Analysis",
        "   → How fair is the trophy-based matchmaking?",
        "   → Are there patterns in opponent matching?",
        "   → Do card levels factor into matchmaking?",
        "",
        "5. Meta Strategy",
        "   → What's the optimal elixir curve?",
        "   → How important is deck diversity (troop/spell balance)?",
        "   → Which rare card combinations dominate?",
        "",
        "6. Time-based Patterns",
        "   → Do win rates vary by time of day?",
        "   → Weekend vs weekday performance differences?",
        "   → Player activity patterns over the 11-day span?",
    ]

    for q in questions:
        print(q)
    print()

def main():
    """Run all analyses"""
    print("\n")
    print("█"*80)
    print(" "*20 + "CLASH ROYALE DATASET ANALYSIS")
    print(" "*25 + "Full Dataset Estimation")
    print("█"*80)
    print()

    estimate_full_dataset_size()
    extrapolate_clan_statistics()
    analyze_data_quality_insights()
    analyze_temporal_insights()
    analyze_competitive_insights()
    clan_engagement_insights()
    research_questions()

    print("="*80)
    print(" NEXT STEPS")
    print("="*80)
    print()
    print("To analyze the full dataset:")
    print("  1. Download dataset.csv (9.87 GB)")
    print("  2. Run: python full_dataset_analysis.py")
    print("  3. Results will be saved to clan_performance_full.csv")
    print()
    print("For memory-constrained environments:")
    print("  • Use chunked reading: pd.read_csv(file, chunksize=100000)")
    print("  • Consider converting to parquet format for faster loading")
    print("  • Use Dask for out-of-core computation")
    print()

if __name__ == "__main__":
    main()
