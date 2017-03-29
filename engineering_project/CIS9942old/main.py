from CIS9942toXLSX import CIS9942toXLSX
from CIS9942toH import CIS9942toH
from CIS9942totxtHeader import CIS9942totxtHeader

import os

for root, directories, filenames in os.walk(b'.'):
    for directory in directories:
        True
        # print( os.path.join(root, directory) )
    for filename in filenames:
        file = os.path.join(root, filename)
        filepath = str(os.path.abspath(file), 'utf-8')
        if not filename.startswith(b'conv') and file.endswith(b'.CAL'):
            print(filepath)

            CIS9942toXLSX(filepath, filename)

            CIS9942toH(filepath, filename)

            CIS9942totxtHeader(filepath, filename)

input("Finished")
