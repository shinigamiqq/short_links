import random
import string


def generate_code(length: int = 6):

    alphabet = string.ascii_letters + string.digits

    return "".join(random.choice(alphabet) for _ in range(length))

