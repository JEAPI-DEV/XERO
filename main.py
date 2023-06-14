import subprocess
from subprocess import Popen
import psutil
import signal
import os
import humanize
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = '48W2943894FW829FOLN398298347FWFHH'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'adminxero!':
            user = User(1)  # use any user ID
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = 'Invalid password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
@login_required
def start():
    # check if voice assistant is already running
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'python3' and 'voiceassistant.py' in proc.cmdline():
            return 'Voice assistant is already running!'
    
    # start voice assistant if not already running
    os.system('python3 voiceassistant.py &')
    #subprocess.Popen(['python3', 'voiceassistant.py'])
    return 'Voice assistant started successfully!'

@app.route('/stop', methods=['POST'])
@login_required
def stop():
    process_name = 'voiceassistant.py'
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.kill()
            return 'Voice assistant stopped successfully!'
    return 'Voice assistant is not running'

@app.route('/restart', methods=['POST'])
@login_required
def restart():
    process_name = 'voiceassistant.py'
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.kill()
    #subprocess.Popen(['python3', 'voiceassistant.py'])
    os.system('python3 voiceassistant.py &')
    return 'Voice assistant restarted successfully!'

@app.route('/processes', methods=['GET', 'POST'])
@login_required
def processes():
    if request.method == 'POST':
        if request.form['action'] == 'kill':
            pid = request.form['pid']
            subprocess.call(['kill', pid])
            message = f'Process {pid} killed.'
        elif request.form['action'] == 'killall':
            subprocess.call(['killall', 'process_name'])
            message = 'All processes killed.'
    else:
        message = None

    proc = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8')
    lines = output.strip().split('\n')
    header = lines.pop(0)
    processes = []
    for line in lines:
        columns = line.split()
        process = {
            'user': columns[0],
            'pid': columns[1],
            'cpu': columns[2],
            'mem': columns[3],
            'vsz': columns[4],
            'rss': columns[5],
            'tty': columns[6],
            'stat': columns[7],
            'start': columns[8],
            'time': columns[9],
            'command': ' '.join(columns[10:])
        }
        processes.append(process)

    meminfo = subprocess.Popen(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)
    memoutput = meminfo.stdout.read().decode('utf-8')
    memtotal = int(memoutput.split('MemTotal:')[1].split(' kB')[0].strip()) * 1024
    memfree = int(memoutput.split('MemFree:')[1].split(' kB')[0].strip()) * 1024
    memused = memtotal - memfree
    mempercent = (memused / memtotal) * 100
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()

    return render_template('processes.html',
                           processes=processes,
                           message=message,
                           memused=humanize.naturalsize(memused),
                           memtotal=humanize.naturalsize(memtotal),
                           mempercent=round(mempercent, 2),
                           cpu_percent=cpu_percent,
                           memory_info=memory_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
