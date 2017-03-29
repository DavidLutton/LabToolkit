import os


def CIS9942totxtHeader(file, name):
    buffer = ""
    with open(file) as f:
        trigger = 0
        for line in f:

            # print(line)
            if trigger == 0:
                # print(line)

                buffer = buffer + line.strip() + "\n"

            if line == '{Data}\n':  # After the data blck begins set trigger = 1
                trigger = 1
    # print(buffer)

    path = os.path.join(os.path.dirname(file), str(name, 'utf-8') + ".header.txt")
    # print(path)
    with open(path, "wt") as out_f:
        out_f.write(buffer)
