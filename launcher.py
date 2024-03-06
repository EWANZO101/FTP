import subprocess
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_exe')
def start_exe():
    exe_path = r"J:\FXServerSV2.exe"  # Replace this with the actual path to your .exe file
    subprocess.Popen(exe_path)
    return 'Executable started successfully.'

@app.route('/stop_exe')
def stop_exe():
    subprocess.call("taskkill /f /im FXServerSV2.exe", shell=True)
    return 'Executable stopped successfully.'

if __name__ == '__main__':
    app.run(debug=True)
