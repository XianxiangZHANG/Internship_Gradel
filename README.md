# Internship_GRADEL
## Database of Gradel
 Auther: Xianxiang ZHANG

Created a database by Django.


### Create migration files:
```
python manage.py makemigrations
```
### Apply migration:
```
python manage.py migrate
```

### Run the project:
```
python manage.py runserver
```

### Run the Celery:
```
celery -A database worker --loglevel=info
celery -A database beat --loglevel=info
```

### Install SQL Server Tool (sqlcmd)

Import Microsoft's GPG key:
```
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
```

Register the Microsoft Ubuntu repository:
```
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list)"
```

Install mssql-tools：
```
sudo apt-get install mssql-tools unixodbc-dev
```

Add sqlcmd to your system path:
Open your shell configuration file (such as .bashrc or .zshrc) and add the following line:
```
export PATH="$PATH:/opt/mssql-tools/bin"
```

Then reload the configuration file:
```
source ~/.bashrc
```

Verify the installation:
Confirm that sqlcmd has been successfully installed and can be called from the command line:
```
sqlcmd -?
```