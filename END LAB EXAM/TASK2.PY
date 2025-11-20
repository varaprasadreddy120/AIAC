#!/usr/bin/env python3
"""
TASK2.PY - Gaming Leaderboard Quick Sort Implementation

AI-assisted Quick Sort algorithm for sorting players by score in a gaming leaderboard.
Features:
- Efficient O(n log n) average case performance
- Stable sorting (preserves order of players with equal scores)
- Random pivot selection to avoid worst-case scenarios
- Configurable ascending/descending order
- Comprehensive documentation and test cases

Requirements:
- Python 3.7+
- No external dependencies (uses only standard library)

Usage:
    # Run demonstration (generates sample leaderboard and sorts it):
    python TASK2.PY
    
    # Run unit tests:
    python TASK2.PY --test
    
    # Use as a module:
    from TASK2 import Player, sort_players
    players = [Player("Alice", 100), Player("Bob", 200)]
    sorted_players = sort_players(players)

Algorithm Details:
- Uses divide-and-conquer approach
- Random pivot selection for better average performance
- Three-way partitioning (less, equal, greater) for stability
- Handles duplicate scores gracefully

Author: AI-Assisted Development
Date: 2024
"""

from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, TypeVar
import random
import unittest

T = TypeVar("T")


@dataclass
class Player:
    name: str
    score: int

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, score={self.score})"


def quick_sort(
    items: Iterable[T],
    key: Optional[Callable[[T], object]] = None,
    reverse: bool = True,
) -> List[T]:
    """
    Stable Quick Sort for a sequence of items.

    Parameters:
    - items: Iterable[T] -- collection of elements to sort (e.g., Player instances).
    - key: Optional[Callable[[T], object]] -- function extracting comparison key from items.
           If None and items are comparable, the items themselves are used.
    - reverse: bool -- if True, sorts in descending order (default, useful for leaderboards).
                       If False, sorts in ascending order.

    Returns:
    - List[T] -- a new list containing the items sorted according to key and reverse.

    Notes:
    - This implementation is stable: elements with equal keys preserve their original order.
    - It uses a divide-and-conquer approach that selects a random pivot to reduce worst-case
      behavior on already-sorted inputs.
    """
    seq = list(items)
    if key is None:
        def keyfn(x): return x  # type: ignore
    else:
        keyfn = key

    # Attach original index to ensure stability in comparisons of equal keys.
    indexed = [(keyfn(x), idx, x) for idx, x in enumerate(seq)]

    def _qsort(arr: List[tuple]) -> List[tuple]:
        """
        Internal recursive Quick Sort function using three-way partitioning.
        
        Algorithm Steps:
        1. Base case: If array has 0 or 1 elements, it's already sorted
        2. Choose a random pivot (helps avoid worst-case O(n²) on sorted data)
        3. Partition into three groups: less than, equal to, greater than pivot
        4. Recursively sort the less and greater groups
        5. Combine: greater + equal + less (for descending) or less + equal + greater (for ascending)
        """
        # Base case: arrays of size 0 or 1 are already sorted
        if len(arr) <= 1:
            return arr
        
        # Step 1: Choose a random pivot to avoid worst-case performance
        # Random pivot selection helps achieve O(n log n) average case
        pivot_index = random.randrange(len(arr))
        pivot_key = arr[pivot_index][0]  # Extract the comparison key

        # Step 2: Three-way partitioning
        # This approach ensures stability (equal elements maintain original order)
        less = []      # Elements with key < pivot
        equal = []     # Elements with key == pivot (preserves stability)
        greater = []   # Elements with key > pivot

        for item in arr:
            item_key = item[0]  # Extract key for comparison
            if item_key < pivot_key:
                less.append(item)
            elif item_key > pivot_key:
                greater.append(item)
            else:
                # Equal keys: preserve original index order for stability
                equal.append(item)

        # Step 3: Recursively sort partitions and combine
        # For leaderboards, default reverse=True means we want descending order:
        if reverse:
            # Higher scores (greater) come first, then equal, then lower scores (less)
            return _qsort(greater) + equal + _qsort(less)
        else:
            # Ascending order: lower scores first
            return _qsort(less) + equal + _qsort(greater)

    sorted_indexed = _qsort(indexed)
    # Extract original items in sorted order
    return [item[2] for item in sorted_indexed]


# Simple convenience wrapper specifically for Player lists
def sort_players(players: Iterable[Player], descending: bool = True) -> List[Player]:
    """
    Sort a list of Player objects by score.

    Parameters:
    - players: Iterable[Player] -- players to sort.
    - descending: bool -- True for highest scores first (leaderboard style).

    Returns:
    - List[Player] -- sorted players.
    """
    return quick_sort(players, key=lambda p: p.score, reverse=descending)


# -------------------------
# Main execution and demonstration
# -------------------------

def generate_sample_players(count: int = 15) -> List[Player]:
    """
    Generate sample player data for demonstration purposes.
    
    Args:
        count: Number of players to generate
        
    Returns:
        List of Player objects with random names and scores
    """
    # Common gaming usernames
    names = [
        "ShadowWarrior", "DragonSlayer", "NightHawk", "FireStorm", "IceQueen",
        "ThunderBolt", "VenomStrike", "PhoenixRise", "StormBreaker", "BladeRunner",
        "CyberNinja", "GhostHunter", "DarkKnight", "LightBringer", "StarChaser",
        "MoonWalker", "SunRider", "WindWhisper", "EarthShaker", "WaterBender"
    ]
    
    # Generate players with varied scores
    players = []
    for i in range(count):
        name = names[i % len(names)] + str(i + 1) if i >= len(names) else names[i]
        # Generate scores between 100 and 10000, with some duplicates
        score = random.randint(100, 10000)
        # Occasionally create duplicate scores to test stability
        if i > 0 and random.random() < 0.2:
            score = players[random.randint(0, i - 1)].score
        players.append(Player(name, score))
    
    return players


def display_leaderboard(players: List[Player], title: str = "Leaderboard") -> None:
    """
    Display a formatted leaderboard table.
    
    Args:
        players: List of Player objects to display
        title: Title for the leaderboard
    """
    print(f"\n{title}")
    print("=" * 70)
    print(f"{'Rank':<6} {'Player Name':<25} {'Score':>10}")
    print("-" * 70)
    
    for rank, player in enumerate(players, 1):
        print(f"{rank:<6} {player.name:<25} {player.score:>10,}")
    
    print("=" * 70)
    print(f"Total Players: {len(players)}\n")


def main():
    """
    Main function to demonstrate the Quick Sort leaderboard sorting.
    Generates sample player data, displays unsorted and sorted leaderboards.
    """
    import sys
    
    print("=" * 70)
    print("Gaming Leaderboard - Quick Sort Demonstration")
    print("=" * 70)
    print()
    
    # Step 1: Generate sample players
    print("Step 1: Generating sample player data...")
    players = generate_sample_players(15)
    print(f"[OK] Generated {len(players)} players with random scores")
    print()
    
    # Step 2: Display unsorted leaderboard
    print("Step 2: Original (Unsorted) Leaderboard:")
    display_leaderboard(players, "Unsorted Players")
    
    # Step 3: Sort using Quick Sort (descending by default)
    print("Step 3: Sorting players by score using Quick Sort algorithm...")
    print("  - Algorithm: Quick Sort (Divide and Conquer)")
    print("  - Pivot Selection: Random (for optimal average performance)")
    print("  - Order: Descending (highest scores first)")
    print("  - Stability: Preserved (players with equal scores keep original order)")
    print()
    
    sorted_players = sort_players(players, descending=True)
    print("[OK] Sorting complete!")
    print()
    
    # Step 4: Display sorted leaderboard
    print("Step 4: Sorted Leaderboard (Top Players):")
    display_leaderboard(sorted_players, "Top Players Leaderboard")
    
    # Step 5: Show top 5 players
    print("Step 5: Top 5 Players:")
    print("-" * 70)
    for rank, player in enumerate(sorted_players[:5], 1):
        medal = "[1st]" if rank == 1 else "[2nd]" if rank == 2 else "[3rd]" if rank == 3 else f"[{rank}th]"
        print(f"  {medal} {player.name:<25} Score: {player.score:,}")
    print()
    
    # Step 6: Demonstrate ascending sort
    print("Step 6: Ascending Sort (Lowest to Highest):")
    ascending_sorted = sort_players(players, descending=False)
    display_leaderboard(ascending_sorted[:5], "Bottom 5 Players (Ascending)")
    
    # Step 7: Statistics
    print("Step 7: Statistics:")
    print("-" * 70)
    scores = [p.score for p in players]
    print(f"  Highest Score: {max(scores):,}")
    print(f"  Lowest Score:  {min(scores):,}")
    print(f"  Average Score: {sum(scores) // len(scores):,}")
    print(f"  Total Players: {len(players)}")
    
    # Count duplicate scores
    score_counts = {}
    for p in players:
        score_counts[p.score] = score_counts.get(p.score, 0) + 1
    duplicates = {score: count for score, count in score_counts.items() if count > 1}
    if duplicates:
        print(f"  Duplicate Scores: {len(duplicates)} (stability preserved in sorting)")
    print()
    
    print("=" * 70)
    print("[OK] Quick Sort demonstration complete!")
    print("=" * 70)


# -------------------------
# Unit tests
# -------------------------
class TestQuickSortLeaderboard(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(sort_players([]), [])

    def test_single(self):
        p = Player("Alice", 100)
        self.assertEqual(sort_players([p]), [p])

    def test_basic_descending(self):
        players = [
            Player("Alice", 150),
            Player("Bob", 200),
            Player("Carol", 100),
        ]
        sorted_players = sort_players(players)
        self.assertEqual([p.name for p in sorted_players], ["Bob", "Alice", "Carol"])

    def test_basic_ascending(self):
        players = [
            Player("Alice", 150),
            Player("Bob", 200),
            Player("Carol", 100),
        ]
        sorted_players = sort_players(players, descending=False)
        self.assertEqual([p.name for p in sorted_players], ["Carol", "Alice", "Bob"])

    def test_ties_preserve_order(self):
        players = [
            Player("P1", 100),
            Player("P2", 200),
            Player("P3", 100),  # same score as P1; P1 came first
            Player("P4", 200),  # same score as P2; P2 came first
        ]
        sorted_players = sort_players(players)
        # expect P2 then P4 (200s in original order), then P1 then P3 (100s in original order)
        self.assertEqual([p.name for p in sorted_players], ["P2", "P4", "P1", "P3"])

    def test_random_compare_builtin_sorted(self):
        # Compare our quick_sort to Python's sorted for correctness on random inputs
        rng = random.Random(0)
        players = [Player(f"Player{i}", rng.randint(0, 1000)) for i in range(200)]
        ours = sort_players(players)
        expected = sorted(players, key=lambda p: p.score, reverse=True)
        # Since our sort is stable and preserves order, they should match exactly on stable sort
        self.assertEqual([p.score for p in ours], [p.score for p in expected])
        # ensure players with same score appear in same relative order
        # we'll compare list of (score, original_index)
        expected_with_idx = []
        for i, p in enumerate(players):
            expected_with_idx.append((p.score, i, p))
        expected_sorted = sorted(expected_with_idx, key=lambda x: (-x[0], x[1]))
        ours_with_idx = []
        for i, p in enumerate(players):
            ours_with_idx.append((p.score, i, p))
        ours_sorted = quick_sort(players, key=lambda p: p.score, reverse=True)
        self.assertEqual([p for (_, _, p) in expected_sorted], ours_sorted)

    def test_non_player_items_with_key(self):
        items = [{"name": "A", "score": 10}, {"name": "B", "score": 30}, {"name": "C", "score": 20}]
        sorted_items = quick_sort(items, key=lambda x: x["score"], reverse=True)
        self.assertEqual([it["name"] for it in sorted_items], ["B", "C", "A"])


if __name__ == "__main__":
    import sys
    
    # Check if user wants to run tests or demo
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Run unit tests
        print("Running unit tests...")
        print("=" * 70)
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # Run main demonstration
        try:
            main()
        except Exception as e:
            print(f"\n[ERROR] Error: {e}")
            import traceback
            traceback.print_exc()
            print("\nTo run unit tests instead, use: python TASK2.PY --test")
            sys.exit(1)