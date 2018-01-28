from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import traceback

test_xls = '题库-guol-20180122.xlsx'

try:
    print(open_workbook(test_xls))

    with open(test_xls, 'rb') as f:
        print(open_workbook(file_contents=mmap(f.fileno(), 0, access=ACCESS_READ)))

    wb = open_workbook(test_xls)

    for s in wb.sheets():
        print('Sheet:', s.name)
        for row in range(s.nrows):
            values = []
            for col in range(s.ncols):
                values.append(s.cell(row, col).value)
            #print(','.join(str(values)))
            print(str(values))
except BaseException as e:
    print(traceback.print_stack())
