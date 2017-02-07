#!/usr/bin/env python3


def dflistfrequencyswithin(df, column="Frequency"):
    frequencys = []
    for index, row in df.iterrows():
        frequencys.append(row[column])
    return(frequencys)


def dfiteronrows(df):
    for index, row in df.iterrows():
        yield(row, index)
