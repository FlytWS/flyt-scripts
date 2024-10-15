import os

os.chdir('/etc/flyt/scripts')
os.system('git reset --hard origin/main')
os.system('git pull')
subprocess.call(['chmod', '-R', '777', '/etc/flyt/scripts'])
