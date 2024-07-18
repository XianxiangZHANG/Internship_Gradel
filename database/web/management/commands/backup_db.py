import os
import shutil
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
import logging

log_file_path = os.path.join(settings.BASE_DIR, 'backups', 'backup.log')

os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file_path)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Command(BaseCommand):
    help = 'Backup the database and delete old backups'

    def add_arguments(self, parser):
        parser.add_argument('--backup-dir', type=str, help='Directory to store backups')
        parser.add_argument('--days-to-keep', type=int, default=1, help='Days to keep the backups')

    def handle(self, *args, **options):
        backup_dir = options.get('backup_dir') or os.path.join(settings.BASE_DIR, 'backups')
        days_to_keep = options.get('days_to_keep')
        os.makedirs(backup_dir, exist_ok=True)
        os.chmod(backup_dir, 0o777)

        db_settings = settings.DATABASES['default']
        db_engine = db_settings['ENGINE']
        db_name = db_settings['NAME']
        timestamp = datetime.now().strftime("%m%d%Y%H%M%S")
        backup_file = os.path.join(backup_dir, f'{db_name}_backup_{timestamp}.bak')

        try:
            if 'postgresql' in db_engine:
                self.backup_postgresql(db_settings, db_name, backup_file)
            elif 'mysql' in db_engine:
                self.backup_mysql(db_settings, db_name, backup_file)
            elif 'sqlite3' in db_engine:
                self.backup_sqlite(db_settings, backup_file)
            elif 'mssql' in db_engine:
                self.backup_mssql(db_settings, db_name, backup_file)
            else:
                self.stdout.write(self.style.ERROR('Unsupported database backend'))
                return

            if os.path.exists(backup_file):
                self.stdout.write(self.style.SUCCESS(f'Database backup created at {backup_file}'))
                logger.info(f'Database backup created at {backup_file}.')
            else:
                self.stdout.write(self.style.ERROR('Failed to create backup file'))
                logger.error('Failed to create backup file.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ERROR:{e}'))
            logger.error(f'ERROR：{e}')

        # Call the method to delete old backups
        self.delete_old_backups(backup_dir, days_to_keep)

    def backup_postgresql(self, db_settings, db_name, backup_file):
        user = db_settings.get('USER', '')
        password = db_settings.get('PASSWORD', '')
        host = db_settings.get('HOST', '')
        port = db_settings.get('PORT', '')
        command = f'PGPASSWORD={password} pg_dump -U {user} -h {host} -p {port} {db_name} > {backup_file}'
        self.run_backup(command)

    def backup_mysql(self, db_settings, db_name, backup_file):
        user = db_settings.get('USER', '')
        password = db_settings.get('PASSWORD', '')
        host = db_settings.get('HOST', '')
        port = db_settings.get('PORT', '')
        command = f'mysqldump -u {user} -p{password} -h {host} -P {port} {db_name} > {backup_file}'
        self.run_backup(command)

    def backup_sqlite(self, db_settings, backup_file):
        db_file = db_settings['NAME']
        command = f'sqlite3 {db_file} .dump > {backup_file}'
        self.run_backup(command)

    def backup_mssql(self, db_settings, db_name, backup_file):
        user = db_settings.get('USER', '')
        password = db_settings.get('PASSWORD', '')
        host = db_settings.get('HOST', '')
        local_backup_file = f'/var/opt/mssql/data/{db_name}_backup_{datetime.now().strftime("%m%d%Y%H%M%S")}.bak'
        command = f'sqlcmd -S {host} -U {user} -P {password} -C -Q "BACKUP DATABASE [{db_name}] TO DISK=\'{local_backup_file}\'"'
        self.run_backup(command, local_backup_file, backup_file)

    def run_backup(self, command, local_file=None, destination_file=None):
        try:
            os.system(command)
            logger.info('Database backup command executed.')
            if local_file and destination_file:
                shutil.move(local_file, destination_file)
                os.chmod(destination_file, 0o777) 
                logger.info(f'Backup file moved from {local_file} to {destination_file}.')
        except Exception as e:
            logger.error(f'Error executing backup command: {e}')
            self.stdout.write(self.style.ERROR(f'Error executing backup command: {e}'))

    def delete_old_backups(self, directory, days_to_keep):
        """Deletes files older than a specified number of days in a directory."""
        now = datetime.now()
        cutoff = now - timedelta(days=days_to_keep)

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_modified < cutoff:
                    os.remove(file_path)
                    logger.info(f"Deleted old backup: {file_path}")
