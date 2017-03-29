from openpyxl import Workbook


def CIS9942toXLSX(file, name):
    wb = Workbook(guess_types=True)

    ws = wb.active

    # print(file)
    # ws = wb.create_sheet(title=file)
    ws.title = name

    with open(file) as f:
        trigger = 0
        for line in f:
            if trigger == 1:
                element = line.split()
                # pprint(element)
                compose = [element[0] + ' ' + element[1],
                           element[2],
                           element[3],
                           element[4],
                           element[5]
                           ]
                # pprint(compose)
                ws.append(compose)

            if line == '{Data}\n':
                trigger = 1

    wb.save(file + ".xlsx")
