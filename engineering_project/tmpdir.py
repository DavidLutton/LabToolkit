import os
import platform
from uuid import uuid4 as uuid  # https://docs.python.org/3.4/library/uuid.html
import shutil


class tmpdir():
    """Create tmpdir for tempory files."""

    def __init__(self):
        if os.name != 'posix':
            # self.tmp = os.path.expanduser("~" + os.sep + os.path.join("", "Temp")) + os.sep + str(uuid())
            self.tmp = os.path.expanduser(os.path.join('~', 'Local Settings', 'Temp', str(uuid)))
        else:
            self.tmp = os.path.expanduser(os.path.join('~', '.cache', 'tmp', str(uuid)))
        print(self.tmp)
        if not os.path.exists(self.tmp):
            os.mkdir(self.tmp)

    # def __enter__(self):
        # return(self.tmp)

    def __del__(self):
        print(self.tmp)
        r = shutil.rmtree(self.tmp)


'''tmp1 = tmp()
print(tmp1.tmp)
del(tmp1)
'''
