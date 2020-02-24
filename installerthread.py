import threading
import time
import functions
import requests
import subprocess

class InstallerThread(threading.Thread):
    def __init__(self, package_name, text_buffer):
        threading.Thread.__init__(self)
        self.package_name = package_name
        self.text_buffer = text_buffer
        self.run_thread = True
        self.script_process  = None

    def terminate(self):
        self.run_thread = False
        if self.script_process != None:
            self.script_process.terminate()

    def run(self):
        self.download_sources()
        print('Download complete')
        time.sleep(0.25)
        self.script_process = subprocess.Popen(['/var/cache/alps/scripts/' + self.package_name + '.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.text_buffer.bind_subprocess(self.script_process)

    def download_sources(self):
        urls = functions.get_download_urls(self.package_name)
        download_dir = '/var/cache/alps/sources/'
        for url in urls:
            self.text_buffer.insert_at_cursor('Downloading  ' + url + '\n')
            parts = url.split('/')
            filename = parts[len(parts) - 1]
            download_path = download_dir + '/' + filename
            self.current_contents = self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter(), True)
            print('Starting Download...')
            to_continue = self.download_url(url, download_path)
            if to_continue == False:
                return

    def download_url(self, url, filename):
        with open(filename, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')
            print('Length: ' + str(total))
            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 8192*1024)):
                    print('.')
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    self.text_buffer.set_text(self.current_contents + '\r[{}{}]'.format('=' * done, ' ' * (50-done)))
                    time.sleep(0.25)
                    if not self.run_thread:
                        return False
        self.text_buffer.insert_at_cursor('\n')

    def run_script_subprocess(self):
        pass
