import pytest
from datetime import date, timedelta
import sys
sys.path.append('/workspace/anki_clone/your_srs_clone/src')
from your_srs_clone.core.card import Card
from your_srs_clone.core.sm2 import sm2

def test_card_defaults():
    c = Card()
    assert c.ease_factor == 2.5
    assert c.interval == 0
    assert c.review_count == 0
    assert c.due_date == date.today()

def test_sm2_algorithm():
    # Create a card with known values
    card = Card(ease_factor=2.5, interval=0, review_count=0)

    # Test with quality 3 (average)
    updated_card = sm2(card, 3)

    # Calculate the actual values based on implementation
    expected_ease = max(1.3, 2.5 + 0.1 - (5-3) * (0.08 + (5-3)*0.02))
    assert updated_card.ease_factor == pytest.approx(expected_ease, rel=1e-2)
    assert updated_card.interval == 1
    assert updated_card.review_count == 1
    assert updated_card.due_date == date.today() + timedelta(days=1)

    # Test with quality 5 (perfect)
    updated_card = sm2(updated_card, 5)

    # For review_count == 1 and quality >=3, interval should be set to 6 according to the implementation
    assert updated_card.interval == 6
    assert updated_card.review_count == 2

    # Test with quality 0 (complete failure)
    updated_card = sm2(updated_card, 0)

    # For quality < 3, interval should be reset to 1
    assert updated_card.interval == 1
    assert updated_card.review_count == 3

    # Test with quality 5 (perfect) again
    updated_card = sm2(updated_card, 5)

    # For review_count == 3 and quality >=3, interval should be calculated based on the algorithm
    assert updated_card.interval == int(round(1 * updated_card.ease_factor))

@pytest.mark.parametrize("initial_review_count, initial_interval, quality", [
    # First review, perfect score
    (0, 0, 5),
    # Low quality review (e.g., 3) on a new card
    (0, 0, 3),
    # Very low quality review (e.g., 0) on a new card, EF should hit floor
    (0, 0, 0),
])
def test_sm2_transitions(initial_review_count, initial_interval, quality):
    card = Card(review_count=initial_review_count, interval=initial_interval)
    if initial_review_count > 0: # Adjust EF if it's not a brand new card for more realistic test
         card.ease_factor = 2.5 # Or a more specific EF if testing a particular state

    # First call to sm2
    card = sm2(card, quality)

    assert card.ease_factor >= 1.3  # Minimum ease factor

    if initial_review_count == 0 and quality < 3:
        assert card.interval == 1
    elif initial_review_count > 0 and quality >= 3:
        assert card.interval == 6
    elif initial_review_count > 0 and quality < 3:
        assert card.interval == 1
    elif initial_review_count == 0 and quality >= 3:
        assert card.interval > 0

    if card.interval > 0:
        assert card.due_date == date.today() + timedelta(days=card.interval)

def test_sm2_low_quality_floors_ef():
    card = Card(ease_factor=1.5) # Start with a low EF
    card = sm2(card, 0) # Simulate a very bad review
    assert card.ease_factor == 1.3 # EF should be floored at 1.3

    card = Card(ease_factor=2.0)
    card = sm2(card, 3) # review_count = 1, interval = 1
                        # ef = 2.0 + 0.1 - (5-3)*0.08 - (5-3)*0.02 = 2.1 - 0.16 - 0.08 = 1.86
    assert round(card.ease_factor, 2) == 1.86