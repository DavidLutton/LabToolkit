#!/usr/bin/env python3

import pandas as pd


def parse(raw):

    data = {}
    colu = []

    flag = False
    for line in raw:
        if flag is False:

            if line.strip().startswith("Col"):
                spl = line.strip().split(".")
                if spl[1].startswith("Title"):
                    # print(line.strip())
                    col = spl[1].split("=")[1]
                    # print(col)
                    colu.append(col)

            if line.startswith("{Data}"):
                # print(colu)
                for each in colu:
                    data[each] = []
                flag = True
        else:
            columns = line.split("\t")
            i = 0
            for each in columns:

                columns[i] = columns[i].strip()  # remove whitespace

                if colu[i] == "Frequency":
                    freq, mul = columns[i].split(" ")
                    dispatch = {
                        "GHz": 1e9,
                        "MHz": 1e6,
                        "kHz": 1e3,
                        "Hz": 1e1,
                    }

                    try:
                        columns[i] = float(freq) * dispatch[mul]
                    except:
                        raise NotImplementedError
                i += 1

            i = 0
            for each in columns:
                data[colu[i]].append(each)
                i += 1
            # print(data)
    # print(len(colu))
    if len(colu) == 7:
        return(pd.DataFrame({
            colu[0]: data[colu[0]],
            colu[1]: data[colu[1]],
            colu[2]: data[colu[2]],
            colu[3]: data[colu[3]],
            colu[4]: data[colu[4]],
        }))
    else:
        raise NotImplementedError
