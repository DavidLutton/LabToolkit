import os
from uuid import uuid4 as uuid  # https://docs.python.org/3.4/library/uuid.html
import shutil


class tmpdir():

    def __init__(self):
        self.tmp = os.path.expanduser("~" + os.sep + os.path.join("Local Settings", "Temp")) + os.sep + str(uuid())
        print(self.tmp)
        if not os.path.exists(self.tmp):
            os.mkdir(self.tmp)

    def __del__(self):
        print(self.tmp)
        r = shutil.rmtree(self.tmp)


'''tmp1 = tmp()
print(tmp1.tmp)
del(tmp1)
'''
