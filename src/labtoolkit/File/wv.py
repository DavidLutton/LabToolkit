import re
from pathlib import Path
import numpy as np

# s = 0.00000000002
# df[df == 0 + 1j * 0] = s + 1j * s  
# consider meddling with zeros to clear divide by zero warning = ~-200 dBm


def read(file):
    wvtext = file.read_text('UTF8', errors='replace')
    wave = re.search(r'WAVEFORM', wvtext).start() 
    data_start = wave + 1 + re.search(r'#', wvtext[wave:wave+50]).start()
    
    header_raw = file.read_bytes()[0:wave-1].decode('UTF8')
    
    data = file.read_bytes()[data_start:-1]
    data = np.frombuffer(data, dtype='<i2')

    data = data / (32767-0.5)  
    # https://www.rohde-schwarz.com/us/faq/example-on-how-to-manually-generate-a-wv-file-with-python-faq_78704-1166336.html
    
    data = data.astype(np.float32)
    data = data.view(np.complex64)
    
    key_end = 0  # stub for linter
    data_begin = 0  # stub for linter
    
    headers = {}
    for index, char in enumerate(header_raw):
        match char:
            case '{':
                block = True
                key_begin = index +1
            case '}':
                data_end = index
                key = header_raw[key_begin:key_end]
                text = header_raw[data_begin:data_end].strip()
                match key:
                    case 'SAMPLES':
                        headers[key] = int(text)
                    case 'CLOCK':
                        headers[key] = float(text)
                    case _:
                        headers[key] = text

            case ':':
                if block == True:
                    key_end = index
                    data_begin = index + 1
                    block = False

    if re.search(r'{WWAVEFORM', wvtext):
        return headers, np.array([0j-0], dtype=np.complex64)
    return headers, data