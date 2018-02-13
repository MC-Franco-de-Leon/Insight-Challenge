# coding: utf-8


# numpy, pandas
import os
import time
import mmap
import math
import numpy as np
import pandas as pd
import re
import datetime
from numpy import median


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d%m%Y')
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be DDMMYYYY")
        return False


def newcontribution(CMTE_ID, NAME, ZIP, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID):
    global df,mdf
    global percentile
    new=0

    if df.loc[(df['NAME'] == NAME) & (df['ZIP'] == ZIP)].empty:
        print('NEW ENTRY')
    else:
        print('New contribution of exixting unique ID*******')
        new=1

    df.loc[len(df)] = [CMTE_ID, NAME, ZIP, TRANSACTION_DT[4:8],TRANSACTION_AMT]  # initialize media and contributions for this entry
    if new==1:
        alltransactions = (df.loc[(df['CMTE_ID'] == CMTE_ID) & (df['ZIP'] == ZIP) & (df['DATE'] == TRANSACTION_DT[4:8]), 'CONTRIBUTION'])
     #   print(type(alltransactions))
        ordertransactions=alltransactions.sort_values(ascending=True)

        ntransactions = int(alltransactions.count())
        print(ntransactions)
        sumtransactions = alltransactions.sum()
        perc=0
        ordinal_rank= math.ceil(percentile*ntransactions/100)
        val=pd.Series(ordertransactions).values
        perc=val[0]



        if mdf.loc[(mdf['CMTE_ID'] == CMTE_ID) & (mdf['ZIP'] == ZIP) & (mdf['DATE'] == TRANSACTION_DT[4:8])].empty:
            mdf.loc[len(mdf)] = [CMTE_ID, ZIP, TRANSACTION_DT[4:8], perc, sumtransactions, int(ntransactions)]
        else:
            mdf.loc[(mdf['CMTE_ID'] == CMTE_ID) & (mdf['ZIP'] == ZIP) & (mdf['DATE'] == TRANSACTION_DT[4:8])]=[CMTE_ID, ZIP, TRANSACTION_DT[4:8], perc, sumtransactions, int(ntransactions)]
        print(mdf)




os.chdir('./input')
per = open('percentile.txt')


lines = per.readlines()
percentile = float(lines[0])
print("percentile:", percentile)
with open('itcont.txt') as f:

    columns = ['CMTE_ID', 'NAME', 'ZIP', 'DATE', 'CONTRIBUTION']
    cols=['CMTE_ID', 'ZIP', 'DATE', 'PERCENTILE','AMOUNT','TRANSACTIONS']
    df = pd.DataFrame(columns=columns, index=[])
    mdf= pd.DataFrame(columns=cols, index=[])

    for line in f:
        x = line.split("|")
        print("")

        if len(x) > 1:
            CMTE_ID = x[0]
            ZIP_CODE = x[10]  # first five digits?
            TRANSACTION_DT = x[13]
            TRANSACTION_AMT = float(x[14])
            OTHER_ID = str(x[15])
            NAME = str(x[7])
            my_list = NAME.split(",")
            aux = 0
            for element in my_list:  # checking valid name
                for char in element:
                    if not char.isalpha() and not char.isspace():
                        aux = 1  # invalid format

            if (OTHER_ID == ""):  # check this is empty
                OTHER_ID = "empty"
                if (CMTE_ID == "") or (TRANSACTION_AMT == ""):
                    aux = 1
                    print('IGNORED bec CMTE_ID or TRANSACTION_AMT is empty')

                elif aux != 1:  # check name is correct:

                    if len(TRANSACTION_DT) == 8:
                        YEAR = TRANSACTION_DT[4:8]
                        DAY = TRANSACTION_DT[2:4]
                        MONTH = TRANSACTION_DT[0:2]
                        date = DAY + MONTH + YEAR
                        print(date)
                        if (validate(DAY + MONTH + YEAR)):  # valid format of date
                            zipcode_string = str(ZIP_CODE)
                            ZIP = zipcode_string[0:5]

                            if len(ZIP) == 5:
                                newcontribution(CMTE_ID, NAME, ZIP, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID)

                                # do something cool
                            else:
                                print('Zip code is incorrect')
                        else:
                            print('transaction date is incorrect')
                    else:
                        print('transaction date is incorrect')
                else:
                    print('NAME format is incorrect')


            else:
                print('EXLUDED ID (non empty):', OTHER_ID)

    os.chdir('..')

    current=os.getcwd()
    os.chdir('./output')
    print("Current: ", os.getcwd())

    np.savetxt(r'repeat_donors.txt', mdf, fmt='%s', delimiter='|')

