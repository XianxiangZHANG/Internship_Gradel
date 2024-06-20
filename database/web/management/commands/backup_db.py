import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Backup the database'

    def handle(self, *args, **kwargs):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default'].get('USER', '')
        db_password = settings.DATABASES['default'].get('PASSWORD', '')
        db_host = settings.DATABASES['default'].get('HOST', '')
        db_port = settings.DATABASES['default'].get('PORT', '')

        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, f'{db_name}_backup_{datetime.now().strftime("%m%d%Y%H%M%S")}.sql')

        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            dump_command = f'pg_dump -U {db_user} -h {db_host} -p {db_port} {db_name} > {backup_file}'
        elif 'mysql' in settings.DATABASES['default']['ENGINE']:
            dump_command = f'mysqldump -u {db_user} -p{db_password} -h {db_host} -P {db_port} {db_name} > {backup_file}'
        elif 'sqlite3' in settings.DATABASES['default']['ENGINE']:
            dump_command = f'sqlite3 {db_name} .dump > {backup_file}'
        else:
            self.stdout.write(self.style.ERROR('Unsupported database backend'))
            return

        os.system(dump_command)
        self.stdout.write(self.style.SUCCESS(f'Database backup created at {backup_file}'))
