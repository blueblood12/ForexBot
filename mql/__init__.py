
def dict_to_string(data: dict) -> str:
    return " ".join(f"{key}: {value}" for key, value in data.items())
