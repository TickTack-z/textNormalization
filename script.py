# -*- coding: utf-8 -*-
__author__ = 'ZFTurbo: https://kaggle.com/zfturbo'

import operator
from num2words import num2words
import json

INPUT_PATH = r"C:\Users\sxzho\Desktop\kaggle\input/"
SUBM_PATH = r"C:\Users\sxzho\Desktop\kaggle/"

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
OTH = str.maketrans("፬", "4")

def solve():
    print('Train start...')
    
    # Work with primary dataset
    file = "en_train.csv"
    train = open(INPUT_PATH + file, encoding='UTF8')
    line = train.readline()
    res = dict()
    total = 0
    not_same = 0
    while 1:
        line = train.readline().strip()
        if line == '':
            break
        total += 1
        pos = line.find('","')
        text = line[pos + 2:]
        if text[:3] == '","':
            continue
        text = text[1:-1]
        arr = text.split('","')
        if arr[0] != arr[1]:
            not_same += 1
        if arr[0] not in res:
            res[arr[0]] = dict()
            res[arr[0]][arr[1]] = 1
        else:
            if arr[1] in res[arr[0]]:
                res[arr[0]][arr[1]] += 1
            else:
                res[arr[0]][arr[1]] = 1
    train.close()
    print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))

    # Work with additional dataset from https://www.kaggle.com/google-nlu/text-normalization
    files = ['output_1.csv', 'output_6.csv', 'output_11.csv', 'output_16.csv', \
        'output_21.csv', 'output_91.csv', 'output_96.csv']

    for file in files:
        train = open(INPUT_PATH + file, encoding='UTF8')
        line = train.readline()
        while 1:
            line = train.readline().strip()
            if line == '':
                break
            line = line.replace(',NA,', ',"NA",')
            total += 1
            pos = line.find('","')
            text = line[pos + 2:]
            if text[:3] == '","':
                continue
            text = text[1:-1]
            arr = text.split('","')
            if arr[0] == '<eos>':
                continue
            if arr[1] != '<self>':
                not_same += 1

            if arr[1] == '<self>' or arr[1] == 'sil':
                arr[1] = arr[0]

            if arr[0] not in res:
                res[arr[0]] = dict()
                res[arr[0]][arr[1]] = 1
            else:
                if arr[1] in res[arr[0]]:
                    res[arr[0]][arr[1]] += 1
                else:
                    res[arr[0]][arr[1]] = 1
        train.close()
        print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))
    
    sdict = {}
    sdict['km2'] = 'square kilometers'
    sdict['km'] = 'kilometers'
    sdict['kg'] = 'kilograms'
    sdict['lb'] = 'pounds'
    sdict['dr'] = 'doctor'
    sdict['m²'] = 'square meters'

    for i,j in res.items():
        if len(j)>=2:
            res[i]=dict()
            res[i][j]=1

    total = 0
    changes = 0
    out = open(SUBM_PATH + 'baseline4_en.csv', "w", encoding='UTF8')
    out.write('"id","after"\n')
    test = open(INPUT_PATH + "en_test.csv", encoding='UTF8')
    line = test.readline().strip()
    while 1:
        line = test.readline().strip()
        if line == '':
            break

        pos = line.find(',')
        i1 = line[:pos]
        line = line[pos + 1:]

        pos = line.find(',')
        i2 = line[:pos]
        line = line[pos + 1:]

        line = line[1:-1]
        out.write('"' + i1 + '_' + i2 + '",')
        if line in res:
            srtd = sorted(res[line].items(), key=operator.itemgetter(1), reverse=True)
            out.write('"' + srtd[0][0] + '"')
            changes += 1
        else:
            # line.split(' ')
            if len(line) > 1:
                val = line.split(',')
                if len(val) == 2 and val[0].isdigit and val[1].isdigit:
                    line = ''.join(val)

            if line.isdigit():
                srtd = line.translate(SUB)
                srtd = srtd.translate(SUP)
                srtd = srtd.translate(OTH)
                out.write('"' + num2words(float(srtd)) + '"')
                changes += 1
            elif len(line.split(' ')) > 1:
                val = line.split(' ')
                for i, v in enumerate(val): 
                    if v.isdigit():
                        srtd = v.translate(SUB)
                        srtd = srtd.translate(SUP)
                        srtd = srtd.translate(OTH)
                        val[i] = num2words(float(srtd))
                    elif v in sdict:
                        val[i] = sdict[v]

                out.write('"' + ' '.join(val) + '"')
                changes += 1
            else:
                out.write('"' + line + '"')

        out.write('\n')
        total += 1

    print('Total: {} Changed: {}'.format(total, changes))
    test.close()
    out.close()

if __name__ == '__main__':
    solve()