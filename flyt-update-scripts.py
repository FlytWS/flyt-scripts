import os

if not os.path.isdir("/etc/flyt/scripts/.git"):    
    os.system('git clone https://github.com/FlytWS/flyt-scripts.git /etc/flyt/scripts/')
else :
    os.chdir('/etc/flyt/scripts')
    os.system('git reset --hard origin/main')
    os.system('git pull')