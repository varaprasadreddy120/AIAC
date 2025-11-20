"""
Unit Tests for Gaming Leaderboard Sorting
==========================================

This module contains comprehensive test cases for the Quick Sort implementation.
Tests cover edge cases, performance, and correctness of the sorting algorithm.

Test Categories:
----------------
1. Basic Sorting Tests
2. Edge Case Tests (empty, single, duplicates)
3. Descending Order Verification
4. Data Integrity Tests
5. Performance Tests

Author: THALLAPELLI SAVIN KUMAR
Date: 20-Nov-2025
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def quick_sort(players_list):
    """Quick Sort function to sort players by score in descending order."""
    if len(players_list) <= 1:
        return players_list
    pivot = players_list[-1]
    pivot_score = pivot["score"]
    left = [player for player in players_list[:-1] if player["score"] >= pivot_score]
    right = [player for player in players_list[:-1] if player["score"] < pivot_score]
    return quick_sort(left) + [pivot] + quick_sort(right)


class TestBasicSorting(unittest.TestCase):
    """Test basic sorting functionality"""
    
    def test_standard_list_sorting(self):
        """Test sorting a standard list of players"""
        players = [
            {"name": "Alice", "score": 1500},
            {"name": "Bob", "score": 3000},
            {"name": "Charlie", "score": 2500},
            {"name": "David", "score": 2000},
            {"name": "Eve", "score": 3500}
        ]
        sorted_players = quick_sort(players)
        scores = [p["score"] for p in sorted_players]
        self.assertEqual(scores, [3500, 3000, 2500, 2000, 1500])
    
    def test_descending_order(self):
        """Verify scores are in descending order"""
        players = [
            {"name": "P1", "score": 100},
            {"name": "P2", "score": 50},
            {"name": "P3", "score": 150}
        ]
        sorted_players = quick_sort(players)
        for i in range(len(sorted_players) - 1):
            self.assertGreaterEqual(
                sorted_players[i]["score"],
                sorted_players[i + 1]["score"]
            )
    
    def test_preserves_player_info(self):
        """Ensure player names are preserved correctly"""
        players = [
            {"name": "Alice", "score": 100},
            {"name": "Bob", "score": 200}
        ]
        sorted_players = quick_sort(players)
        self.assertEqual(sorted_players[0]["name"], "Bob")
        self.assertEqual(sorted_players[1]["name"], "Alice")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_empty_list(self):
        """Test sorting an empty list"""
        result = quick_sort([])
        self.assertEqual(result, [])
    
    def test_single_player(self):
        """Test sorting a list with one player"""
        players = [{"name": "Solo", "score": 500}]
        result = quick_sort(players)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Solo")
    
    def test_two_players(self):
        """Test sorting a list with two players"""
        players = [
            {"name": "Low", "score": 100},
            {"name": "High", "score": 200}
        ]
        result = quick_sort(players)
        self.assertEqual(result[0]["name"], "High")
        self.assertEqual(result[1]["name"], "Low")
    
    def test_duplicate_scores(self):
        """Test sorting with duplicate scores"""
        players = [
            {"name": "A", "score": 500},
            {"name": "B", "score": 500},
            {"name": "C", "score": 500}
        ]
        result = quick_sort(players)
        self.assertEqual(len(result), 3)
        scores = [p["score"] for p in result]
        self.assertEqual(scores, [500, 500, 500])
    
    def test_already_sorted(self):
        """Test sorting an already sorted list"""
        players = [
            {"name": "A", "score": 300},
            {"name": "B", "score": 200},
            {"name": "C", "score": 100}
        ]
        result = quick_sort(players)
        scores = [p["score"] for p in result]
        self.assertEqual(scores, [300, 200, 100])
    
    def test_reverse_sorted(self):
        """Test sorting a reverse sorted list"""
        players = [
            {"name": "A", "score": 100},
            {"name": "B", "score": 200},
            {"name": "C", "score": 300}
        ]
        result = quick_sort(players)
        scores = [p["score"] for p in result]
        self.assertEqual(scores, [300, 200, 100])


class TestZeroAndNegativeScores(unittest.TestCase):
    """Test handling of zero and negative scores"""
    
    def test_zero_scores(self):
        """Test sorting with zero scores"""
        players = [
            {"name": "A", "score": 0},
            {"name": "B", "score": 100},
            {"name": "C", "score": 0}
        ]
        result = quick_sort(players)
        scores = [p["score"] for p in result]
        self.assertEqual(scores, [100, 0, 0])
    
    def test_negative_scores(self):
        """Test sorting with negative scores"""
        players = [
            {"name": "A", "score": -10},
            {"name": "B", "score": 50},
            {"name": "C", "score": -5}
        ]
        result = quick_sort(players)
        scores = [p["score"] for p in result]
        self.assertEqual(scores, [50, -5, -10])
    
    def test_mixed_positive_negative(self):
        """Test sorting with mixed positive and negative scores"""
        players = [
            {"name": "A", "score": 100},
            {"name": "B", "score": -50},
            {"name": "C", "score": 0},
            {"name": "D", "score": -20}
        ]
        result = quick_sort(players)
        scores = [p["score"] for p in result]
        self.assertEqual(scores, [100, 0, -20, -50])


class TestLargeDatasets(unittest.TestCase):
    """Test with larger datasets"""
    
    def test_100_players(self):
        """Test sorting 100 players"""
        players = [{"name": f"Player{i}", "score": i} for i in range(100)]
        result = quick_sort(players)
        self.assertEqual(len(result), 100)
        scores = [p["score"] for p in result]
        # Verify descending order
        for i in range(len(scores) - 1):
            self.assertGreaterEqual(scores[i], scores[i + 1])
    
    def test_1000_players(self):
        """Test sorting 1000 players"""
        import random
        scores = list(range(1000))
        random.shuffle(scores)
        players = [{"name": f"P{i}", "score": scores[i]} for i in range(1000)]
        result = quick_sort(players)
        result_scores = [p["score"] for p in result]
        self.assertEqual(result_scores, sorted(scores, reverse=True))
    
    def test_random_shuffle(self):
        """Test with randomly shuffled large dataset"""
        import random
        base_scores = [1000, 500, 2000, 300, 1500, 2500, 100, 1200, 800, 1800]
        random.shuffle(base_scores)
        players = [{"name": f"Player{i}", "score": base_scores[i]} for i in range(len(base_scores))]
        result = quick_sort(players)
        result_scores = [p["score"] for p in result]
        expected = sorted(base_scores, reverse=True)
        self.assertEqual(result_scores, expected)


class TestDataIntegrity(unittest.TestCase):
    """Test that data integrity is maintained"""
    
    def test_no_data_loss(self):
        """Ensure no players are lost during sorting"""
        players = [
            {"name": "Alice", "score": 1500},
            {"name": "Bob", "score": 3000},
            {"name": "Charlie", "score": 2500}
        ]
        result = quick_sort(players)
        self.assertEqual(len(result), len(players))
    
    def test_all_players_present(self):
        """Verify all original players are in sorted list"""
        players = [
            {"name": "Alice", "score": 1500},
            {"name": "Bob", "score": 3000},
            {"name": "Charlie", "score": 2500},
            {"name": "David", "score": 2000}
        ]
        result = quick_sort(players)
        result_names = set(p["name"] for p in result)
        original_names = set(p["name"] for p in players)
        self.assertEqual(result_names, original_names)
    
    def test_no_duplicate_creation(self):
        """Ensure no extra duplicates are created"""
        players = [
            {"name": "A", "score": 100},
            {"name": "B", "score": 200}
        ]
        result = quick_sort(players)
        self.assertEqual(len(result), len(players))


class TestCustomAttributes(unittest.TestCase):
    """Test with additional player attributes"""
    
    def test_extra_attributes_preserved(self):
        """Ensure extra attributes are preserved"""
        players = [
            {"name": "Alice", "score": 1500, "level": 10, "rank": "Gold"},
            {"name": "Bob", "score": 3000, "level": 15, "rank": "Platinum"},
            {"name": "Charlie", "score": 2500, "level": 12, "rank": "Silver"}
        ]
        result = quick_sort(players)
        # Check that Bob (highest score) has his attributes
        self.assertEqual(result[0]["level"], 15)
        self.assertEqual(result[0]["rank"], "Platinum")
    
    def test_sort_ignores_other_attributes(self):
        """Verify sorting only uses score, not other attributes"""
        players = [
            {"name": "A", "score": 100, "level": 20},
            {"name": "B", "score": 200, "level": 5},
            {"name": "C", "score": 150, "level": 30}
        ]
        result = quick_sort(players)
        scores = [p["score"] for p in result]
        self.assertEqual(scores, [200, 150, 100])


class TestLeaderboardDisplay(unittest.TestCase):
    """Test leaderboard display scenarios"""
    
    def test_top_3_leaderboard(self):
        """Test getting top 3 players"""
        players = [
            {"name": "A", "score": 100},
            {"name": "B", "score": 500},
            {"name": "C", "score": 300},
            {"name": "D", "score": 400},
            {"name": "E", "score": 200}
        ]
        sorted_players = quick_sort(players)
        top_3 = sorted_players[:3]
        names = [p["name"] for p in top_3]
        self.assertEqual(names, ["B", "D", "C"])
    
    def test_bottom_player(self):
        """Test getting the lowest scoring player"""
        players = [
            {"name": "Winner", "score": 1000},
            {"name": "Loser", "score": 10}
        ]
        sorted_players = quick_sort(players)
        self.assertEqual(sorted_players[-1]["name"], "Loser")


class TestSortStability(unittest.TestCase):
    """Test stability of sorting with equal scores"""
    
    def test_equal_scores_all_present(self):
        """Test that all players with equal scores are present"""
        players = [
            {"name": "A", "score": 100},
            {"name": "B", "score": 100},
            {"name": "C", "score": 100}
        ]
        result = quick_sort(players)
        names = set(p["name"] for p in result)
        self.assertEqual(names, {"A", "B", "C"})


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)