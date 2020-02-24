from threading import Thread
import requests

class Downloader(Thread):
    def __init__(self, url, filename, buffer, thread_group, on_completion, pkg_name):
        Thread.__init__(self)
        self.url = url
        self.filename = filename
        self.run_thread = True
        self.buffer = buffer
        self.thread_group = thread_group
        self.thread_group.append(self)
        self.on_completion = on_completion
        self.pkg_name = pkg_name

    def run(self):
        with open(self.filename, 'wb') as f:
            response = requests.get(self.url, stream=True)
            total = response.headers.get('content-length')
            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 8192*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    if not self.run_thread:
                        return
                    self.update_buffer('\r[{}{}]'.format('=' * done, ' ' * (50-done)))
        self.update_buffer('\n')
        status = True
        for t in self.thread_group:
            if t != self and t.isAlive():
                status = False
                break
        if status:
            print('All Threads completed...')
            self.on_completion(self.pkg_name)

    def update_buffer(self, content):
        self.buffer.insert_at_cursor(content)
        #self.buffer.textview.scroll_to_mark(self.buffer.get_insert(), 0.0, True, 0.5, 0.5)