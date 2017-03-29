def results(file):
    header = ""
    data = []
    trigger = 0
    
    with open(file) as f:
        for line in f:
            if trigger == 0:
                header = header + line.strip() + "\n"
            if trigger == 1:
                data.append(line.strip().split('\t'))
                
            if line == '{Data}\n':  # After the data blck begins set trigger = 1
                trigger = 1

    columns = []
    for each in filter(lambda x: '.Title' in x, header.split('\n')):
        columns.append(each.split('=')[1])

    return(header, data, columns)

'''path = os.path.join(os.path.dirname(file), str(name, 'utf-8') + ".head")
    with open(path, "wt") as out_f:
        out_f.write(buffer)
'''

def harmonise(data, columns):
    #for i, item in enumerate(columns):
    #data[i] = func(item)
    #print(i)
    #print(item)
    # http://stackoverflow.com/questions/3173915/modification-of-the-list-items-in-the-loop-python

    for i, item in enumerate(data):
        #print(item)
        for h, header in enumerate(columns):
            
            if header == 'Frequency':
                # item[h] = 1000
                frequency = item[h].split(' ')
                if frequency[1] == "kHz":
                    mul = 1e3
                if frequency[1] == "MHz":
                    mul = 1e6
                if frequency[1] == "GHz":
                    mul = 1e9
                hz = mul * float(frequency[0])
                #mhz = "{:.6f}" .format(hz / 1e6)  # freq in MHz to 6dp
                item[h] = hz / 1e6

            if header in [ 'RF Stress', 'Generator Level', 'Fwd Pwr', 'Cal Level' ]:
                item[h] = float(item[h])
            if header in [ 'Time', ]:
                item[h] = item[h].strip()
        
    
    return(data, columns)

def ordercolumns(data, columns):
    return(data, columns)


