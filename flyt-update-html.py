import os
import subprocess

os.chdir('/var/www/html')
os.system('git reset --hard origin/main')
os.system('git pull')
subprocess.call(['chmod', '-R', '777', '/var/www/html'])
