import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
path = BASE_DIR / 'trade_records'


async def save_to_csv(name: str, data: dict):
    file_path = path / f"{name}.csv"
    exists = file_path.exists()
    with open(file_path, 'a', newline='') as file:
        fields = list(data.keys())
        writer = csv.DictWriter(file, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow(data)
