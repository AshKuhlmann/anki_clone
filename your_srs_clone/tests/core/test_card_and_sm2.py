import pytest
from datetime import date, timedelta
from your_srs_clone.core.card import Card
from your_srs_clone.core.sm2 import sm2

def test_card_initialization():
    card = Card()
    assert card.ease_factor == 2.5
    assert card.interval == 0
    assert card.review_count == 0
    assert card.due_date == date.today()

def test_sm2_algorithm():
    # Create a card with known values
    card = Card(ease_factor=2.5, interval=0, review_count=0)

    # Test with quality 3 (average)
    updated_card = sm2(card, 3)

    assert updated_card.ease_factor == pytest.approx(2.58, rel=1e-2)
    assert updated_card.interval == 1
    assert updated_card.review_count == 1
    assert updated_card.due_date == date.today() + timedelta(days=1)

    # Test with quality 5 (perfect)
    updated_card = sm2(updated_card, 5)

    assert updated_card.ease_factor == pytest.approx(2.68, rel=1e-2)
    assert updated_card.interval == pytest.approx(2.68, rel=1e-2)
    assert updated_card.review_count == 2
    assert updated_card.due_date == date.today() + timedelta(days=int(round(2.68)))

    # Test with quality 0 (complete failure)
    updated_card = sm2(updated_card, 0)

    assert updated_card.ease_factor == pytest.approx(1.3, rel=1e-2)
    assert updated_card.interval == 1
    assert updated_card.review_count == 3
    assert updated_card.due_date == date.today() + timedelta(days=1)