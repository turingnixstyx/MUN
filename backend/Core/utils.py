import subprocess
import os
from backend.settings import BASE_DIR
import datetime


def perform_database_backup():
    current_date = datetime.date.today()
    current_hour = datetime.datetime.now().time().hour
    print("Current date Current time", current_date, current_hour)

    backup_folder = os.path.join(
        BASE_DIR,
        'backups'
    )

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    backup_path = os.path.join(
        backup_folder,
        '{}_{}_logs.json'.format(current_date, current_hour)
    )

    subprocess.run([
        'python', 'manage.py', 'dumpdata', '--output', backup_path
    ])

    print(f"{current_date}_{current_hour}_logs.json backup ran successfully!")
