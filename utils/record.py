import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.resolve()
path = BASE_DIR / 'trade_records'


def change_name(name: str):
    return ' '.join(c.title() for c in name.split('_'))


async def save_to_csv(name: str, data: dict):
    file_path = path / f"{name}.csv"
    exists = file_path.exists()
    data['time'] = str(datetime.utcnow().time())
    with open(file_path, 'a', newline='') as file:
        names = [change_name(name) for name in data.keys()]
        writer = csv.DictWriter(file, fieldnames=names)
        if not exists:
            writer.writeheader()
        writer.writerow(data)


async def update_csv(name: str, data: dict):
    file_path = path / f"{name}.csv"
    exists = file_path.exists()
    if not exists:
        return
    # with open(file_path, 'a', newline='') as file:
        # reader = csv.DictReader(file)
        # for row in reader:

async def get_orders(name: str):
    file_path = path / f"{name}.csv"
    exists = file_path.exists()
    if not exists:
        return
    with open(file_path, 'a', newline='') as file:
        reader = csv.DictReader(file)
        return [row['Order'] for row in reader]
