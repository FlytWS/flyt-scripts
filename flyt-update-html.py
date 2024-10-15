import os

os.chdir('/var/www/html')
os.system('git reset --hard origin/main')
os.system('git pull')