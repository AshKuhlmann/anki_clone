from datetime import date, timedelta
from .card import Card

def sm2(card: Card, quality: int) -> Card:
    # Ensure quality is within the expected range (0-5)
    if not 0 <= quality <= 5:
        raise ValueError("Quality must be an integer between 0 and 5.")

    # update ease factor
    card.ease_factor = max(1.3, card.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)) # Original SM-2 formula variation

    # increment review count
    card.review_count += 1

    # compute next interval
    if quality < 3: # If quality is less than 3, reset review count for interval calculation
        card.interval = 1 # Reset interval to 1 day for failed reviews
        # Optionally, you might want to reset review_count or handle it differently
    elif card.review_count == 1:
        card.interval = 1
    elif card.review_count == 2:
        card.interval = 6
    else:
        card.interval = int(round(card.interval * card.ease_factor)) # Round to nearest int

    # Ensure interval is at least 1 if quality >=3
    if quality >=3 and card.interval < 1:
        card.interval = 1

    # set new due date
    card.due_date = date.today() + timedelta(days=card.interval)
    return card