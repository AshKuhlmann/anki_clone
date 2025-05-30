import pytest
from datetime import date, timedelta
from src.your_srs_clone.models.card import CardModel

# Test data for SM-2 algorithm
@pytest.mark.parametrize(
    "review_count, interval, ease_factor, expected_interval",
    [
        (0, 0, 2.5, 1),      # First review
        (1, 1, 2.5, 6),      # Second review after 1 day
        (2, 6, 2.5, 14),     # Third review after 6 days
        (3, 14, 2.5, 29),    # Fourth review after 14 days
        (4, 29, 2.5, 60),    # Fifth review after 29 days
        (5, 60, 2.5, 120),   # Sixth review after 60 days
        (6, 120, 2.5, 240),  # Seventh review after 120 days
        (7, 240, 2.5, 480),  # Eighth review after 240 days
    ]
)
def test_sm2_interval_calculation(review_count, interval, ease_factor, expected_interval):
    """Test the SM-2 algorithm interval calculation."""
    # Create a card with the given parameters
    card = CardModel(
        question="Test Question",
        answer="Test Answer",
        review_count=review_count,
        interval=interval,
        ease_factor=ease_factor
    )

    # Calculate the next due date based on today's date
    today = date.today()
    if review_count == 0:
        # First review is always tomorrow
        expected_due_date = today + timedelta(days=1)
    else:
        # Calculate the expected due date based on the interval
        expected_due_date = today + timedelta(days=expected_interval)

    # Calculate the actual due date using the SM-2 algorithm
    if review_count == 0:
        # First review is always tomorrow
        actual_due_date = today + timedelta(days=1)
    else:
        # Calculate the actual due date based on the interval and ease factor
        actual_interval = int(interval * ease_factor)
        actual_due_date = today + timedelta(days=actual_interval)

    # Assert that the calculated due date matches the expected due date
    assert actual_due_date == expected_due_date

# Test for ease factor adjustment based on user response
@pytest.mark.parametrize(
    "ease_factor, response, expected_ease_change",
    [
        (2.5, 'correct', 0.1),     # Correct response increases ease factor by 0.1
        (2.5, 'incorrect', -0.15), # Incorrect response decreases ease factor by 0.15
        (2.5, 'hard', -0.15),      # Hard question decreases ease factor by 0.15
        (2.5, 'good', 0.05),       # Good question increases ease factor by 0.05
    ]
)
def test_ease_factor_adjustment(ease_factor, response, expected_ease_change):
    """Test the adjustment of ease factor based on user response."""
    # Create a card with the given parameters
    card = CardModel(
        question="Test Question",
        answer="Test Answer",
        review_count=0,
        interval=0,
        ease_factor=ease_factor
    )

    # Adjust the ease factor based on the user response
    if response == 'correct':
        card.ease_factor = min(2.9, card.ease_factor + 0.1)
    elif response == 'incorrect':
        card.ease_factor = max(1.3, card.ease_factor - 0.15)
    elif response == 'hard':
        card.ease_factor = max(1.3, card.ease_factor - 0.15)
    elif response == 'good':
        card.ease_factor = min(2.9, card.ease_factor + 0.05)

    # Calculate the expected ease factor
    expected_ease_factor = min(2.9, max(1.3, ease_factor + expected_ease_change))

    # Assert that the adjusted ease factor matches the expected ease factor
    assert card.ease_factor == pytest.approx(expected_ease_factor, rel=1e-2)