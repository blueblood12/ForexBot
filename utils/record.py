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
    data['date'] = datetime.utcnow().strftime("%d/%m/%Y %H:%M")
    with open(file_path, 'a', newline='') as file:
        data = {change_name(name): value for name, value in data.items()}
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(data)


async def update_csv(name: str, data: dict):
    file = path / f"{name}.csv"
    temp = path / "tmp.csv"
    exists = file.exists()
    if not exists:
        return
    with open(file, 'r', newline='') as read, open(temp, 'w', newline='') as write:
        reader = csv.DictReader(read)
        writer = csv.DictWriter(write, fieldnames=data['fieldnames'])
        writer.writeheader()
        for row in reader:
            if (order := int(row['Order'])) in data:
                row |= data[order]
                writer.writerow(row)
                continue
            writer.writerow(row)
    Path(temp).replace(file)


async def get_orders(name: str):
    file_path = path / f"{name}.csv"
    exists = file_path.exists()
    if not exists:
        return
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        dates = []
        orders = []
        for row in reader:
            try:
                # dates.append(datetime.strptime(row["Date"], "%Y-%m-%d %H:%M:%S.%f"))
                dates.append(float(row["Timestamp"]))
                orders.append(int(row["Order"]))
            except Exception as exp:
                print(exp)
                continue
        else:
            fieldnames = list(row.keys())
        return min(dates), orders, fieldnames

# get_orders("FingerTrapScalper")
