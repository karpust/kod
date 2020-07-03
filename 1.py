import pandas as pd
import sys
from io import StringIO
import csv
from datetime import datetime


st = ''
with open('1.sdr', 'r') as f:
    for line in f:
        st = st + line[0:4] + ',' + line[4:20] + ',' + line[20:36] + ',' + line[36:52] + ',' + line[52:68] + ',' + line[68:84] + '\n'
st = st.replace(' ', '')

st = StringIO(st)

tab1 = pd.read_csv(st, sep=',', header=None)
tab2 = pd.read_csv("1.top", sep="\s+", header=None)

tab1 = tab1.drop([2, 3, 4], axis=1)
tab2 = tab2.drop([1, 5, 6, 7], axis=1)


# tab2 = tab2.pivot_table(tab2, aggfunc=np.mean)
# tab2 = tab2.round({2: 3})


# который даже позволяет вам иметь различную точность для каждого столбца
# df.round({'Alabama_exp':2, 'Credit_exp':3})


tab2.columns = [1, 2, 3, 4]

tab2 = tab2.round(3)


tab1 = tab1.applymap(str)
tab2 = tab2.applymap(str)

# t1 = tab1.dtypes
# t2 = tab2.dtypes

new_tab = pd.merge(tab1, tab2, on=[1])
new_tab = new_tab[[0, 1, 2, 3, 4, 5]]

# new_tab = new_tab.applymap(lambda x: str(x).ljust(16))
# new_tab.columns = new_tab.columns.map(lambda x: str(x).ljust(16))

nt = new_tab[[0]].applymap(lambda x: str(x).ljust(4))
ntb = new_tab[[1,2,3,4,5]].applymap(lambda x: str(x).rjust(16))



nt['tmp'] = 1
ntb['tmp'] = 1

new_tab = pd.merge(nt, ntb, on=['tmp'])
new_tab = new_tab.drop('tmp', axis=1)

# new_tab.columns = new_tab.columns.map(lambda x: str(x).ljust(16))

nt1 = new_tab.dtypes

nt2 = new_tab.dtypes

new_tab[1] = new_tab[1].replace(',', '')


name_file = 'file.csv'
new_tab.to_csv(name_file, index=False, header=False, sep=";")


csv_file = name_file
txt_file = 'survey ' + datetime.now().strftime("%d_%m_%y") + '.sdr'
with open(txt_file, "w") as sdr1:
    with open(csv_file, "r") as csv1:
        [sdr1.write((" ".join(row)+'\n').replace(';', '')) for row in csv.reader(csv1)]
    sdr1.close()
