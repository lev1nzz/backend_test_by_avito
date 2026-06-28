import random
import string


all_chars = list(string.ascii_letters + string.digits)

# функция генерации короткой ссылки
def generate_short_url(all_chars: list[str]):
    short_url_slug = ''

    for _ in range(6):
        short_url_slug += random.choice(all_chars)
        
    return short_url_slug
