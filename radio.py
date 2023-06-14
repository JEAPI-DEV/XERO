import subprocess

def play_radio(url):
    cmd = ['vlc', '--no-video', url]
    subprocess.Popen(cmd)
