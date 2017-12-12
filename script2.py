# -*- coding: utf-8 -*-

import operator
from num2words import num2words
import json
import pandas as pd
from convert import convertDate
from collections import Counter
from subprocess import check_output
import inflect
import re
from subprocess import check_output
p = inflect.engine()
#from Neerja
# Checking if key is decimal or digit or general numeric
def is_num(key):
    if is_float(key) or re.match(r'^-?[0-9]\d*?$', key.replace(',','')): return True
    else: return False

def is_float(string):
    try:
        return float(string.replace(',','')) and "." in string # True if string is a number contains a dot
    except ValueError:  # String is not a number
        return False

def cardinal(key):
    try:
        text = p.number_to_words(key,decimal='point',andword='', zero='o')
        if re.match(r'^0\.',key): 
            text = 'zero '+text[2:]
        if re.match(r'.*\.0$',key): text = text[:-2]+' zero'
        text = text.replace('-',' ').replace(',','')
        return text.lower()
    except: return key

def digit(x): 
    try:
        x = re.sub('[^0-9]', '',x)
        result_string = ''
        for i in x:
            result_string = result_string + cardinal(i) + ' '
        result_string = result_string.strip()
        return result_string
    except:
        return(x) 

#new new new
def url2word(key):
    try:
        key = key.replace('.',' dot ').replace('/',' slash ').replace('-',' dash ').replace(':',' colon ').replace('_',' underscore ')
        key = key.split()
        lis2 = ['dot','slash','dash','colon']
        for i in range(len(key)):
            if key[i] not in lis2:
                key[i]=" ".join(key[i])
        text = " ".join(key)
        return text.lower()
    except:
        return key

#Comprehensive list of all measures
dict_m = {'"': 'inches', "'": 'feet', 'km/s': 'kilometers per second', 'AU': 'units', 'BAR': 'bars', 'CM': 'centimeters', 'mm': 'millimeters', 'FT': 'feet', 'G': 'grams', 
     'GAL': 'gallons', 'GB': 'gigabytes', 'GHZ': 'gigahertz', 'HA': 'hectares', 'HP': 'horsepower', 'HZ': 'hertz', 'KM':'kilometers', 'km3': 'cubic kilometers',
     'KA':'kilo amperes', 'KB': 'kilobytes', 'KG': 'kilograms', 'KHZ': 'kilohertz', 'KM²': 'square kilometers', 'KT': 'knots', 'KV': 'kilo volts', 'M': 'meters',
      'KM2': 'square kilometers','Kw':'kilowatts', 'KWH': 'kilo watt hours', 'LB': 'pounds', 'LBS': 'pounds', 'MA': 'mega amperes', 'MB': 'megabytes',
     'KW': 'kilowatts', 'MPH': 'miles per hour', 'MS': 'milliseconds', 'MV': 'milli volts', 'kJ':'kilojoules', 'km/h': 'kilometers per hour',  'V': 'volts', 
     'M2': 'square meters', 'M3': 'cubic meters', 'MW': 'megawatts', 'M²': 'square meters', 'M³': 'cubic meters', 'OZ': 'ounces',  'MHZ': 'megahertz', 'MI': 'miles',
     'MB/S': 'megabytes per second', 'MG': 'milligrams', 'ML': 'milliliters', 'YD': 'yards', 'au': 'units', 'bar': 'bars', 'cm': 'centimeters', 'ft': 'feet', 'g': 'grams', 
     'gal': 'gallons', 'gb': 'gigabytes', 'ghz': 'gigahertz', 'ha': 'hectares', 'hp': 'horsepower', 'hz': 'hertz', 'kWh': 'kilo watt hours', 'ka': 'kilo amperes', 'kb': 'kilobytes', 
     'kg': 'kilograms', 'khz': 'kilohertz', 'km': 'kilometers', 'km2': 'square kilometers', 'km²': 'square kilometers', 'kt': 'knots','kv': 'kilo volts', 'kw': 'kilowatts', 
     'lb': 'pounds', 'lbs': 'pounds', 'm': 'meters', 'm2': 'square meters','m3': 'cubic meters', 'ma': 'mega amperes', 'mb': 'megabytes', 'mb/s': 'megabytes per second', 
     'mg': 'milligrams', 'mhz': 'megahertz', 'mi': 'miles', 'ml': 'milliliters', 'mph': 'miles per hour','ms': 'milliseconds', 'mv': 'milli volts', 'mw': 'megawatts', 'm²': 'square meters',
     'm³': 'cubic meters', 'oz': 'ounces', 'v': 'volts', 'yd': 'yards', 'µg': 'micrograms', 'ΜG': 'micrograms', 'kg/m3': 'kilograms per meter cube'}

def measure(key):
    try:
        unit = dict_m[key.split()[-1]]
        val = key.split()[0]
        if is_num(val):
            val = num2word(val)
            text = val + ' ' + unit
        else: text = key
        return text
    except:
        return key


def decimal(key):
    try:
        key = float(key.replace(',',''))
        key = p.number_to_words(key,decimal='point',andword='', zero='o')
        if 'o' == key.split()[0]:
            key = key[2:]
        key = key.replace('-',' ').replace(',','')
        return key.lower()
    except:
        return key

def currency(key):
    try:
        v = key.replace('$','').replace('US$','').split()
        if len(v) == 2: 
            if is_num(v[0]):
                text = num2word(v[0]) + ' '+ v[1] + ' '+ 'dollars'
        elif is_num(v[0]):
            text = num2word(v[0]) + ' '+ 'dollars'
        else:
            if 'm' in key or 'M' in key or 'million':
                text = p.number_to_words(key).replace(',','').replace('-',' ').replace(' and','') + ' million dollars'
            elif 'bn' in key:
                text = p.number_to_words(key).replace(',','').replace('-',' ').replace(' and','') + ' billion dollars'
            else: text = key
        return text.lower()
    except:
        return key

dict_mon = {'jan': "January", "feb": "February", "mar ": "march", "apr": "april", "may": "may ","jun": "june", "jul": "july", "aug": "august","sep": "september",
            "oct": "october","nov": "november","dec": "december", "january":"January", "february":"February", "march":"march","april":"april", "may": "may", 
            "june":"june","july":"july", "august":"august", "september":"september", "october":"october", "november":"november", "december":"december"}
def date2word(key):
    v =  key.split('-')
    if len(v)==3:
        if v[1].isdigit():
            try:
                date = datetime.strptime(key , '%Y-%m-%d')
                text = 'the '+ p.ordinal(p.number_to_words(int(v[2]))).replace('-',' ')+' of '+datetime.date(date).strftime('%B')
                if int(v[0])>=2000 and int(v[0]) < 2010:
                    text = text  + ' '+digit2word(v[0])
                else: 
                    text = text + ' ' + digit2word(v[0][0:2]) + ' ' + digit2word(v[0][2:])
            except:
                text = key
            return text.lower()    
    else:   
        v = re.sub(r'[^\w]', ' ', key).split()
        if v[0].isalpha():
            try:
                if len(v)==3:
                    text = dict_mon[v[0].lower()] + ' '+ p.ordinal(p.number_to_words(int(v[1]))).replace('-',' ')
                    if int(v[2])>=2000 and int(v[2]) < 2010:
                        text = text  + ' '+digit2word(v[2])
                    else: 
                        text = text + ' ' + digit2word(v[2][0:2]) + ' ' + digit2word(v[2][2:])   
                elif len(v)==2:

                    if int(v[1])>=2000 and int(v[1]) < 2010:
                        text = dict_mon[v[0].lower()]  + ' '+ digit2word(v[1])
                    else: 
                        if len(v[1]) <=2:
                            text = dict_mon[v[0].lower()] + ' ' + digit2word(v[1])
                        else:
                            text = dict_mon[v[0].lower()] + ' ' + digit2word(v[1][0:2]) + ' ' + digit2word(v[1][2:])
                else: text = key
            except: text = key
            return text.lower()
        else: 
            key = re.sub(r'[^\w]', ' ', key)
            v = key.split()
            try:
                date = datetime.strptime(key , '%d %b %Y')
                text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+ dict_mon[v[1].lower()]
                if int(v[2])>=2000 and int(v[2]) < 2010:
                    text = text  + ' '+digit2word(v[2])
                else: 
                    text = text + ' ' + digit2word(v[2][0:2]) + ' ' + digit2word(v[2][2:])
            except:
                try:
                    date = datetime.strptime(key , '%d %B %Y')
                    text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+ dict_mon[v[1].lower()]
                    if int(v[2])>=2000 and int(v[2]) < 2010:
                        text = text  + ' '+digit2word(v[2])
                    else: 
                        text = text + ' ' + digit2word(v[2][0:2]) + ' ' + digit2word(v[2][2:])
                except:
                    try:
                        date = datetime.strptime(key , '%d %m %Y')
                        text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+datetime.date(date).strftime('%B')
                        if int(v[2])>=2000 and int(v[2]) < 2010:
                            text = text  + ' '+digit2word(v[2])
                        else: 
                            text = text + ' ' + digit2word(v[2][0:2]) + ' ' + digit2word(v[2][2:])
                    except:
                        try:
                            date = datetime.strptime(key , '%d %m %y')
                            text = 'the '+ p.ordinal(p.number_to_words(int(v[0]))).replace('-',' ')+' of '+datetime.date(date).strftime('%B')
                            v[2] = datetime.date(date).strftime('%Y')
                            if int(v[2])>=2000 and int(v[2]) < 2010:
                                text = text  + ' '+digit2word(v[2])
                            else: 
                                text = text + ' ' + digit2word(v[2][0:2]) + ' ' + digit2word(v[2][2:])
                        except:text = key
            return text.lower()         
#old old old

def letters(x):
    try:
        x = re.sub('[^a-zA-Z]', '', x)
        x = x.lower()
        result_string = ''
        for i in range(len(x)):
            result_string = result_string + x[i] + ' '
        return(result_string.strip())  
    except:
        return x

def rom_to_int(string):

    table=[['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]]
    returnint=0
    for pair in table:


        continueyes=True

        while continueyes:
            if len(string)>=len(pair[0]):

                if string[0:len(pair[0])]==pair[0]:
                    returnint+=pair[1]
                    string=string[len(pair[0]):]

                else: continueyes=False
            else: continueyes=False

    return returnint    
def ordinal(x):
    try:
        result_string = ''
        x = x.replace(',', '')
        x = x.replace('[\.]$', '')
        if re.match('^[0-9]+$',x):
            x = num2words(int(x), ordinal=True)
            return(x.replace('-', ' '))
        if re.match('.*V|X|I|L|D',x):
            if re.match('.*th|st|nd|rd',x):
                x = x[0:len(x)-2]
                x = rom_to_int(x)
                result_string = re.sub('-', ' ',  num2words(x, ordinal=True))
            else:
                x = rom_to_int(x)
                result_string = 'the '+ re.sub('-', ' ',  num2words(x, ordinal=True))
        else:
            x = x[0:len(x)-2]
            result_string = re.sub('-', ' ',  num2words(float(x), ordinal=True))
        return(result_string)  
    except:
        return x

def address(x):
    try:
        x = re.sub('[^0-9a-zA-Z]+', '', x)
        result_string = ''
        for i in range(0,len(x)):
            if re.match('[A-Z]|[a-z]',x[i]):
                result_string = result_string + plain(x[i]).lower() + ' '
            else:
                result_string = result_string + cardinal(x[i]) + ' '
                
        return(result_string.strip())        
    except:    
        return(x)    

def telephone(key):
    try:
        key = key.replace('-','.').replace(')','.')
        text = p.number_to_words(key,group =1, decimal = "sil",zero = 'o').replace(',','')
        return text.lower()
    except:    
        return(key)    

INPUT_PATH = r"C:\Users\sxzho\Desktop\kaggle\input/"
SUBM_PATH = r"C:\Users\sxzho\Desktop\kaggle/"

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
OTH = str.maketrans("፬", "4")
labels=['PLAIN', 'PUNCT', 'DATE', 'LETTERS', 'CARDINAL', 'VERBATIM', 'DECIMAL','MEASURE', 'MONEY', 'ORDINAL', 'TIME', 'ELECTRONIC', 'DIGIT','FRACTION', 'TELEPHONE', 'ADDRESS']
labels_dict=dict(zip(labels,range(len(labels))))


def solve():
    print('Train start...')

    '''
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
        pos = line.find(',"')
        text = line[pos + 1:]
        text = text[1:-1]
        arr = text.split('","')
        #arr[0]: type
        #arr[1]: original
        #arr[2]: new
        arr[0]=labels_dict[arr[0]]
        if arr[1] != arr[2]:
            not_same += 1
        if arr[1] not in res:
            res[arr[1]] = dict()
            res[arr[1]][arr[0]]=dict()
            res[arr[1]][arr[0]][arr[2]] = 1
        else:
            if arr[0] in res[arr[1]]:
                if arr[2] not in res[arr[1]][arr[0]]:
                    res[arr[1]][arr[0]][arr[2]] = 1
                else:
                    res[arr[1]][arr[0]][arr[2]] += 1
            else:
                res[arr[1]][arr[0]]=dict()
                res[arr[1]][arr[0]][arr[2]] = 1
    train.close()
    print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))

    # Work with additional dataset from https://www.kaggle.com/google-nlu/text-normalization
    #files = ['output_1.csv', 'output_6.csv', 'output_11.csv', 'output_16.csv', 'output_21.csv', 'output_91.csv', 'output_96.csv']
    files = []

    for file in files:
        train = open(INPUT_PATH + file, encoding='UTF8')
        line = train.readline()
        while 1:
            #arr[0]: type
            #arr[1]: original
            #arr[2]: new
            line = train.readline().strip()
            if line == '':
                break
            line = line.replace(',NA,', ',"NA",')
            total += 1
            if text[:3] == '","':
                continue
            line=line[1:-1]
            arr = line.split('","')

            if arr[0] not in labels_dict:
                continue
            arr[0]=labels_dict[arr[0]]
            if arr[1] == '<eos>':
                continue
            if arr[2] != '<self>':
                not_same += 1

            if arr[2] == '<self>' or arr[2] == 'sil':
                arr[2] = arr[1]

            if arr[1] not in res:
                res[arr[1]] = dict()
                res[arr[1]][arr[0]]=dict()
                res[arr[1]][arr[0]][arr[2]] = 1
            else:
                if arr[0] in res[arr[1]]:
                    if arr[2] not in res[arr[1]][arr[0]]:
                        res[arr[1]][arr[0]][arr[2]] = 1
                    else:
                        res[arr[1]][arr[0]][arr[2]] += 1
                else:
                    res[arr[1]][arr[0]]=dict()
                    res[arr[1]][arr[0]][arr[2]] = 1
        train.close()
        print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))

    import json
    with open('data_short.json', 'w') as fp:
        json.dump(res, fp)
    '''
    import json
    with open('data.json', 'r') as fp:
        res = json.load(fp)

    sdict = {}
    sdict['km2'] = 'square kilometers'
    sdict['km'] = 'kilometers'
    sdict['kg'] = 'kilograms'
    sdict['lb'] = 'pounds'
    sdict['dr'] = 'doctor'
    sdict['m²'] = 'square meters'


    total = 0
    changes = 0
    out = open(SUBM_PATH + 'baseline4_en.csv', "w", encoding='UTF8')
    out.write('"id","after"\n')
    test = open(r"C:\Users\sxzho\Desktop\kaggle\test\label.csv", encoding='ISO-8859-1')
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

        #label sign
        pos = line.find(',')
        i3=""
        if line[-2]==",":
            i3=line[-1]
            line=line[1:-3]
        else:
            i3=line[-2:]
            line=line[1:-4]

        out.write('"' + i1 + '_' + i2 + '",')
        if line in res:
            if i3 in res[line]:
                srtd = sorted(res[line][i3].items(), key=operator.itemgetter(1), reverse=True)
                out.write('"' + srtd[0][0] + '"')
                changes += 1
            else:
                if labels[int(i3)]=="DATE":
                    try:
                        temp=convertDate(line)
                        out.write('"' + temp + '"')
                    except:
                        count=Counter()
                        for x in res[line]:
                            count += Counter(res[line][x])
                        srtd = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
                        out.write('"' + srtd[0][0] + '"')
                count=Counter()
                for x in res[line]:
                    count += Counter(res[line][x])
                srtd = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
                out.write('"' + srtd[0][0] + '"')
        else:   
            if labels[int(i3)]=="DATE":
                try:
                    temp=convertDate(line)
                    out.write('"' + temp + '"')
                    out.write('\n')
                    total += 1
                    continue
                except:
                    out.write('"' + line + '"')
                    out.write('\n')
                    total += 1
                    continue
            elif labels[int(i3)]=="TELEPHONE":
                temp=telephone(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="CARDINAL":
                temp=cardinal(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="DIGIT":
                temp=digit(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="LETTERS":
                temp=letters(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="ORDINAL":
                temp=ordinal(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="ADDRESS":
                temp=ordinal(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="DECIMAL":
                temp=decimal(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="MEASURE":
                temp=measure(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
            elif labels[int(i3)]=="ELECTRONIC":
                temp=url2word(line)
                out.write('"' + temp + '"')
                out.write('\n')
                total += 1
                continue
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
