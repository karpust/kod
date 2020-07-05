import pandas as pd
from io import StringIO
import csv
import easygui
import sys


try:
    sourse_sdr = easygui.fileopenbox(msg='Выберите исходный SDR файл',
                                 filetypes=["*.sdr"], default='C:/*.sdr')
    p = sourse_sdr.split('\\')
    p.pop()
    path_sdr = '\\'.join(p)
except Exception:
    sys.exit()

sourse_top = easygui.fileopenbox(msg='Выберите исходный TOP файл',
                                 filetypes=["*.top"], default=path_sdr + '\\*.top')
st = ''
with open(sourse_sdr, 'r') as f:
    for line in f:
        st = st + line[0:4] + ',' + line[4:20] + ',' + line[68:84] + '\n'
st = StringIO(st)

tab1 = pd.read_csv(st, sep=',', names=[0, 1, 5], header=None)
tab1 = tab1.applymap(str)

try:
    tab2 = pd.read_csv(sourse_top, sep='\s+', names=[1, 0, 2, 3, 4, 5, 6, 7], header=None)
except Exception:
    quit()

tab2 = tab2.drop([0, 5, 6, 7], axis=1)
tab2 = tab2.round(3)
tab2 = tab2.applymap(lambda x: str(x).rjust(16))

new_tab = tab1.merge(tab2, on=1)
new_tab = new_tab[[0, 1, 2, 3, 4, 5]]

name_csv = 'file.csv'
new_tab.to_csv(name_csv, index=False, header=False, sep=";")

sourse_sdr = sourse_sdr.split('\\').pop()
sourse_top = sourse_top.split('\\').pop()

txt_file = 'add_kod ' + sourse_sdr  # source_top.split('.')[0] + datetime.now().strftime("%d_%m_%y") + '.sdr'
# full_path_sdr = os.path.join(path_sdr, txt_file)
full_path_sdr = path_sdr + '\\' + txt_file
with open(full_path_sdr, "w") as sdr1:
    with open(name_csv, "r") as csv1:
        [sdr1.write((" ".join(row)+'\n').replace(';', '')) for row in csv.reader(csv1)]
    sdr1.close()
