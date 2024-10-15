import os

if not os.path.isdir("/var/www/html/.git"):    
    os.system('git clone https://github.com/FlytWS/flyt-html.git /var/www/html/')
else :
    os.chdir('/var/www/html')
    os.system('git reset --hard origin/main')
    os.system('git pull')