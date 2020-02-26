import threading
import time
import functions
import requests
import subprocess
import os
import signal

class UpdaterThread(threading.Thread):
    def __init__(self, url, text_buffer):
        threading.Thread.__init__(self)
        self.text_buffer = text_buffer
        self.run_thread = True
        self.script_process  = None
        self.url = url

    def terminate(self):
        self.run_thread = False
        os.killpg(os.getpgid(self.script_process.pid), signal.SIGTERM)

    def run(self):
        for package_name in self.package_names:
            if self.run_thread == False:
                return
            self.script_process = subprocess.Popen(['/var/lib/alpsui/updater.sh', url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid)
            self.text_buffer.bind_subprocess(self.script_process)
            self.script_process.wait()
        self.text_buffer.append_text('\n\nUpdate Complete. Please restart the system for updates to take effect.')
