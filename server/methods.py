import json
import datetime

class LogManager(object):

    def __init__(self, logfile_name):
        self.logfile_name = logfile_name
    
    def info(self, code, path, headers, body):
        with open(self.logfile_name, 'a+') as file:
            data = {
                'timestamp': datetime.datetime.now().timestamp(),
                'code': str(code),
                'path': str(path),
                'headers': str(headers),
                'body': str(body),
            }
            json.dump(data, file)
            file.write('\n')
    
    def error(self, code, path, headers, error):
        with open(self.logfile_name, 'a+') as file:
            data = {
                'timestamp': datetime.datetime.now().timestamp(),
                'code': str(code),
                'path': str(path),
                'headers': str(headers),
                'error': str(error),
            }
            json.dump(data, file)
            file.write('\n')

    def get_log(self):
        with open(self.logfile_name, 'r+') as file:
            return file.read()