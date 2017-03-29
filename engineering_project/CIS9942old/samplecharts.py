from openpyxl import Workbook
wb = Workbook()
ws = wb.active
for i in range(10):
     ws.append([i])

from openpyxl.chart import BarChart, Reference, Series
values = Reference(ws, min_col=1, min_row=1, max_col=1, max_row=10)
chart = BarChart()
chart.add_data(values)
ws.add_chart(chart)
wb.save("SampleChart.xlsx")
