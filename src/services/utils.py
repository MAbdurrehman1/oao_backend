from io import StringIO
from typing import BinaryIO
import random
import string

import pandas as pd

from cexceptions import EntityProcessException


def uploaded_csv_to_df(file: BinaryIO) -> pd.DataFrame:
    try:
        file_string = file.read().decode("utf-8")
        df = pd.read_csv(
            StringIO(file_string),
        )
    except Exception:
        raise EntityProcessException(entity="CSV File")
    return df


def generate_random_string(length: int, use_letters=True, use_digits=True) -> str:
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string
