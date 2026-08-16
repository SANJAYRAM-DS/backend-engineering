BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num: int) -> str:
    """Converts a positive integer ID into a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    arr = []
    base = len(BASE62_ALPHABET)
    while num > 0:
        rem = num % base
        arr.append(BASE62_ALPHABET[rem])
        num //= base
    arr.reverse()
    return "".join(arr)


def decode_base62(string: str) -> int:
    """Decodes a Base62 string back into an integer ID."""
    base = len(BASE62_ALPHABET)
    num = 0
    for char in string:
        if char not in BASE62_ALPHABET:
            raise ValueError(f"Invalid Base62 character: {char}")
        num = num * base + BASE62_ALPHABET.index(char)
    return num