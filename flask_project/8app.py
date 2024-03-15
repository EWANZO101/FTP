from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import psutil

app = Flask(__name__)

# Path to the FXServerSV3.exe
server_exe_path = "K:\\FXServerSV3.exe"
# Variable to keep track of server status
server_running = False

def get_system_usage():
    # Get RAM, CPU, and Disk usage
    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    disk_usage = psutil.disk_usage('K:\\').percent  # Specific disk usage for K drive
    return ram_usage, cpu_usage, disk_usage

def check_server_status():
    global server_running
    # Check if the process is running
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'FXServerSV3.exe':
            server_running = True
            return
    server_running = False

@app.route('/')
def index():
    global server_running
    check_server_status()
    server_status = "Running" if server_running else "Stopped"
    server_details = "Server Details: Your server details here"
    return render_template('svindex.html', server_running=server_running, server_status=server_status, server_details=server_details)

@app.route('/start', methods=['POST'])
def start_server():
    global server_running
    if not server_running:
        subprocess.Popen([server_exe_path])
        server_running = True
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_server():
    global server_running
    if server_running:
        subprocess.Popen(['taskkill', '/F', '/IM', 'FXServerSV3.exe'])
        server_running = False
    return redirect(url_for('index'))

@app.route('/status')
def status():
    global server_running
    check_server_status()
    return {"status": "running"} if server_running else {"status": "stopped"}

@app.route('/usage')
def usage():
    ram_usage, cpu_usage, disk_usage = get_system_usage()
    return jsonify({"ram_usage": ram_usage, "cpu_usage": cpu_usage, "disk_usage": disk_usage})

import subprocess

@app.route('/launch_ftp', methods=['GET'])
def launch_ftp():
    ftp_program = request.args.get('ftp_program')
    if ftp_program == 'winscp':
        subprocess.Popen([r"C:\Program Files (x86)\WinSCP\WinSCP.exe"])
    elif ftp_program == 'mobaxterm':
        subprocess.Popen([r"C:\Program Files (x86)\Mobatek\MobaXterm\MobaXterm.exe"])
    elif ftp_program == 'filezilla':
        subprocess.Popen([r"C:\Program Files\FileZilla FTP Client\filezilla.exe"])
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5008)
