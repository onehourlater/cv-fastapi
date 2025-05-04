import re
import random
import string

from app.config import AppSettings


def generate_random_string(length: int = 6) -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def check_if_slug_is_valid(slug: str) -> bool:
    if not re.match(AppSettings.CV_SLUG_PATTERN, slug):
        return False

    return True
