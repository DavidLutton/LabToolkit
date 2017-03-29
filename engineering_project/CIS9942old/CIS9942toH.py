import os

from CIS9942toHeader import HEADER as HEADER


def CIS9942toH(file, name):

    with open(file) as f:
        f.readline()  # readline and ignore first line
        title = f.readline().strip()  # Get title remove line encodeing

    buffer = """IMMUNITY TYPE  : CONDUCTED
TITLE   : """ + title + HEADER

    with open(file) as f:
        trigger = 0
        for line in f:

            # print(line)
            if trigger == 1:  # After tiggger = 1, process lines of data
                # print(line)
                data = line.strip()
                data = data.split("\t")

                freq = data[0].split(" ")
                if freq[1] == "kHz":
                    mul = 1e3
                if freq[1] == "MHz":
                    mul = 1e6
                if freq[1] == "GHz":
                    mul = 1e9
                hz = mul * float(freq[0])
                mhz = hz / 1e6

                output = [
                    "{:.6f}" .format(mhz),  # freq im MHz to 6dp
                    str(data[2].strip(' ')),  # V/m
                    str(data[3].strip(' ')),  # Gen level
                    str(data[4].strip(' ')),  # Power forward
                    "999",
                    "999",
                ]
                buffer = buffer + ",".join(output) + "\n"

            if line == '{Data}\n':  # After the data blck begins set trigger = 1
                trigger = 1
    # print(buffer)
    buffer = buffer[:-1]  # Slice off last n characters of string, context.eg line encoding

    path = os.path.join(os.path.dirname(file), "conv-" + str(name, 'utf-8'))
    # print(path)
    with open(path, "wt") as out_f:
        out_f.write(buffer)
