"""
This file contains functions to abbreviate standard street types,
street directions, and numbered streets (e.g. 32nd ave) to words (thirty-second avenue)
Right now it half handles french numbers -
'1re' goes to 'first', etc
Also to go the other way, text number to number
-Joseph
"""

import re

LONG_SUB_EN = {
    'avenue': 'av',
    'ave': 'av',
    'boulevard': 'blvd',
    'by-pass': 'bypass',
    'circle': 'cir',
    'circuit': 'circt',
    'concession': 'conc',
    'crescent': 'cres',
    'corners': 'crnrs',
    'crossing': 'cross',
    'crossroad': 'crossrd',
    'court': 'crt',
    'diversion': 'divers',
    'drive': 'dr',
    'esplanada': 'espl',
    'estates': 'estate',
    'expressway': 'expy',
    'extension': 'exten',
    'freeway': 'fwy',
    'gardens': 'gdns',
    'harbour': 'harbr',
    'grounds': 'grnds',
    'highlands': 'hghlds',
    'heights': 'hts',
    'highway': 'hwy',
    'laneway': 'lanewy',
    'lookout': 'lkout',
    'limits': 'lmts',
    'mountain': 'mtn',
    'orchard': 'orch',
    'passage': 'pass',
    'park': 'pk',
    'parkway': 'pky',
    'place': 'pl',
    'plateau': 'plat',
    'promenade': 'prom',
    'point': 'pt',
    'pathway': 'ptway',
    'private': 'pvt',
    'road': 'rd',
    'range': 'rg',
    'route': 'rte',
    'rightofway': 'rtofwy',
    'section': 'sectn',
    'sideroad': 'siderd',
    'square': 'sq',
    'street': 'st',
    'subdivision': 'subdiv',
    'terrace': 'terr',
    'townline': 'tline',
    'tournabout': 'trnabt',
    'village': 'villge'
}

DIRS_EN = {
    'east': 'e',
    'west': 'w',
    'north': 'n',
    'south': 's',
    'northeast': 'ne',
    'north-east': 'ne',
    'northwest': 'nw',
    'north-west': 'nw',
    'southeast': 'se',
    'south-east': 'se',
    'southwest': 'sw',
    'south-west': 'sw'
}

LONG_SUB_FR = {
    'autoroute': 'aut',
    'avenue': 'av',
    'boulevard': 'boul',
    'barrage': 'brge',
    'centre': 'c',
    'carré': 'car',
    'cul-de-sac': 'cds',
    'chemin': 'ch',
    'carrefour': 'carref',
    'croissant': 'crois',
    'échangeur': 'éch',
    'esplanada': 'espl',
    'impasse': 'imp',
    'passage': 'pass',
    'plateau': 'plat',
    'promenade': 'prom',
    'rond-point': 'rdpt',
    'ruelle': 'rle',
    'route': 'rte',
    'sentier': 'sent',
    'terrasse': 'tsse',
    'ave': 'av'
}

DIRS_FR = {
    'est': 'e',
    'ouest': 'o',
    'nord': 'n',
    'sud': 's',
    'nordest': 'ne',
    'nord-est': 'ne',
    'nordouest': 'no',
    'nord-ouest': 'no',
    'sudest': 'se',
    'sud-est': 'se',
    'sudouest': 'so',
    'sud-ouest': 'so'
}

type_list = list(LONG_SUB_EN.values())
type_list.append('ave')

type_list_fr = list(LONG_SUB_FR.values())
type_list_fr.append('rue')


def AddressClean_en(df, name_in, name_out):
    dirs = DIRS_EN
    long_sub = LONG_SUB_EN
    # get rid of periods
    df[name_out] = [x.replace('.', '') for x in df[name_in].astype('str')]
    # make all lower case
    df[name_out] = df[name_out].str.lower()

    # Loop through directions and  shorten as required:
    for i, j in dirs.items():
    
        # shorten directions only if they are the last word of the string
        expr = r"\b"+re.escape(i)+r"$"
        df[name_out] = df[name_out].replace(regex=expr, value=j)
        # shorten directions if they are first word in string:
        expr = r"^"+re.escape(i)+r"\b"
        df[name_out] = df[name_out].replace(regex=expr, value=j)

    # Loop through road types and shorten as required:
    # FOR ENGLISH

    for i, j in long_sub.items():
        # shorten street types if they are last word:
        expr = r"\b"+re.escape(i)+r"$"
        df[name_out] = df[name_out].replace(regex=expr, value=j)

        # shorten street types if the last word is 'e','n','s',or 'w',
        # and the matched expression immediately precedes it
        for longdir, shortdir in dirs.items():
            expr = r"\b"+re.escape(i)+" "+re.escape(shortdir)+r"$"
            sub = j+" "+shortdir
            df[name_out] = df[name_out].replace(regex=expr, value=sub)
        
    return df
# FOR FRENCH


def Type_Drop_en(df, name_in, name_out):
    df[name_out] = df[name_in]
    for shortdir in DIRS_EN.values():
        expr = r"\b"+re.escape(shortdir)+r"$"
        df[name_out] = df[name_out].replace(regex=expr, value='')
    df[name_out] = df[name_out].str.strip()
    for i in type_list:
        expr = r"\b"+re.escape(i)+r"$"
        df[name_out] = df[name_out].replace(regex=expr, value='')
    df[name_out] = df[name_out].str.strip()
    return df


def Type_Drop_fr(df, name_in, name_out):
    df[name_out] = df[name_in]
    for shortdir in DIRS_FR.values():  # drop if last part
        expr = r"\b"+re.escape(shortdir)+r"$"
        df[name_out] = df[name_out].replace(regex=expr, value='')
    df[name_out] = df[name_out].str.strip()
    for i in type_list:  # drop if first part
        expr = r"^"+re.escape(i)+r"$"
        df[name_out] = df[name_out].replace(regex=expr, value='')
    df[name_out] = df[name_out].str.strip()
    return df


def AddressClean_fr(df, name_in, name_out):
    long_sub = LONG_SUB_FR
    dirs = DIRS_FR

    # get rid of periods
    df[name_out] = [x.replace('.', '') for x in df[name_in].astype('str')]
    df[name_out] = df[name_out].str.lower()

    for i, j in dirs.items():
        # shorten directions only if they are the last word of the string
        expr = r"\b"+re.escape(i)+r"$"
        df[name_out] = df[name_out].replace(regex=expr, value=j)
         
    for i, j in long_sub.items():
        # shorten street types if they are first word in string:
        expr = r"^"+re.escape(i)+r"\b"
        df[name_out] = df[name_out].replace(regex=expr, value=j)

    return df


NUM_DICT_1 = {
    '1st': 'first',
    '2nd': 'second',
    '3rd': 'third',
    '4th': 'fourth',
    '5th': 'fifth',
    '6th': 'sixth',
    '7th': 'seventh',
    '8th': 'eighth',
    '9th': 'ninth',
    '10th': 'tenth',
    '11th': 'eleventh',
    '12th': 'twelfth',
    '13th': 'thirteenth',
    '14th': 'fourteenth',
    '15th': 'fifteenth',
    '16th': 'sixteenth',
    '17th': 'seventeenth',
    '18th': 'eighteenth',
    '19th': 'nineteenth',
    '20th': 'twentieth',
    '21st': 'twenty-first',
    '22nd': 'twenty-second',
    '23rd': 'twenty-third',
    '24th': 'twenty-fourth',
    '25th': 'twenty-fifth',
    '26th': 'twenty-sixth',
    '27th': 'twenty-seventh',
    '28th': 'twenty-eighth',
    '29th': 'twenty-ninth',
    '30th': 'thirtieth',
    '31st': 'thirty-first',
    '32nd': 'thirty-second',
    '33rd': 'thirty-third',
    '34th': 'thirty-fourth',
    '35th': 'thirty-fifth',
    '36th': 'thirty-sixth',
    '37th': 'thirty-seventh',
    '38th': 'thirty-eighth',
    '39th': 'thirty-ninth',
    '40th': 'fourtieth',
    '41st': 'forty-first',
    '42nd': 'forty-second',
    '43rd': 'forty-third',
    '44th': 'forty-fourth',
    '45th': 'forty-fifth',
    '46th': 'forty-sixth',
    '47th': 'forty-seventh',
    '48th': 'forty-eighth',
    '49th': 'forty-ninth',
    '50th': 'fiftieth',
    '51st': 'fifty-first',
    '52nd': 'fifty-second',
    '53rd': 'fifty-third',
    '54th': 'fifty-fourth',
    '55th': 'fifty-fifth',
    '56th': 'fifty-sixth',
    '57th': 'fifty-seventh',
    '58th': 'fifty-eighth',
    '59th': 'fifty-ninth',
    '60th': 'sixtieth',
    '61st': 'sixty-first',
    '62nd': 'sixty-second',
    '63rd': 'sixty-third',
    '64th': 'sixty-fourth',
    '65th': 'sixty-fifth',
    '66th': 'sixty-sixth',
    '67th': 'sixty-seventh',
    '68th': 'sixty-eighth',
    '69th': 'sixty-ninth',
    '70th': 'seventieth',
    '71st': 'seventy-first',
    '72nd': 'seventy-second',
    '73rd': 'seventy-third',
    '74th': 'seventy-fourth',
    '75th': 'seventy-fifth',
    '76th': 'seventy-sixth',
    '77th': 'seventy-seventh',
    '78th': 'seventy-eighth',
    '79th': 'seventy-ninth',
    '80th': 'eightieth',
    '81st': 'eighty-first',
    '82nd': 'eighty-second',
    '83rd': 'eighty-third',
    '84th': 'eighty-fourth',
    '85th': 'eighty-fifth',
    '86th': 'eighty-sixth',
    '87th': 'eighty-seventh',
    '88th': 'eighty-eighth',
    '89th': 'eighty-ninth',
    '90th': 'ninetieth',
    '91st': 'ninety-first',
    '92nd': 'ninety-second',
    '93rd': 'ninety-third',
    '94th': 'ninety-fourth',
    '95th': 'ninety-fifth',
    '96th': 'ninety-sixth',
    '97th': 'ninety-seventh',
    '98th': 'ninety-eighth',
    '99th': 'ninety-ninth',
    '1re': 'first',
    '2e': 'second',
    '3e': 'third',
    '4e': 'fourth',
    '5e': 'fifth',
    '6e': 'sixth',
    '7e': 'seventh',
    '8e': 'eighth',
    '9e': 'ninth',
    '10e': 'tenth',
    '11e': 'eleventh',
    '12e': 'twelfth',
    '13e': 'thirteenth',
    '14e': 'fourteenth',
    '15e': 'fifteenth',
    '16e': 'sixteenth',
    '17e': 'seventeenth',
    '18e': 'eighteenth',
    '19e': 'nineteenth',
    '20e': 'twentieth',
    '21e': 'twenty-first',
    '22e': 'twenty-second',
    '23e': 'twenty-third',
    '24e': 'twenty-fourth',
    '25e': 'twenty-fifth',
    '26e': 'twenty-sixth',
    '27e': 'twenty-seventh',
    '28e': 'twenty-eighth',
    '29e': 'twenty-ninth',
    '30e': 'thirtieth',
    '31e': 'thirty-first',
    '32e': 'thirty-second',
    '33e': 'thirty-third',
    '34e': 'thirty-fourth',
    '35e': 'thirty-fifth',
    '36e': 'thirty-sixth',
    '37e': 'thirty-seventh',
    '38e': 'thirty-eighth',
    '39e': 'thirty-ninth',
    '40e': 'fortieth',
    '41e': 'forty-first',
    '42e': 'forty-second',
    '43e': 'forty-third',
    '44e': 'forty-fourth',
    '45e': 'forty-fifth',
    '46e': 'forty-sixth',
    '47e': 'forty-seventh',
    '48e': 'forty-eighth',
    '49e': 'forty-ninth',
    '50e': 'fiftieth',
    '51e': 'fifty-first',
    '52e': 'fifty-second',
    '53e': 'fifty-third',
    '54e': 'fifty-fourth',
    '55e': 'fifty-fifth',
    '56e': 'fifty-sixth',
    '57e': 'fifty-seventh',
    '58e': 'fifty-eighth',
    '59e': 'fifty-ninth',
    '60e': 'sixtieth',
    '61e': 'sixty-first',
    '62e': 'sixty-second',
    '63e': 'sixty-third',
    '64e': 'sixty-fourth',
    '65e': 'sixty-fifth',
    '66e': 'sixty-sixth',
    '67e': 'sixty-seventh',
    '68e': 'sixty-eighth',
    '69e': 'sixty-ninth',
    '70e': 'seventieth',
    '71e': 'seventy-first',
    '72e': 'seventy-second',
    '73e': 'seventy-third',
    '74e': 'seventy-fourth',
    '75e': 'seventy-fifth',
    '76e': 'seventy-sixth',
    '77e': 'seventy-seventh',
    '78e': 'seventy-eighth',
    '79e': 'seventy-ninth',
    '80e': 'eightieth',
    '81e': 'eighty-first',
    '82e': 'eighty-second',
    '83e': 'eighty-third',
    '84e': 'eighty-fourth',
    '85e': 'eighty-fifth',
    '86e': 'eighty-sixth',
    '87e': 'eighty-seventh',
    '88e': 'eighty-eighth',
    '89e': 'eighty-ninth',
    '90e': 'ninetieth',
    '91e': 'ninety-first',
    '92e': 'ninety-second',
    '93e': 'ninety-third',
    '94e': 'ninety-fourth',
    '95e': 'ninety-fifth',
    '96e': 'ninety-sixth',
    '97e': 'ninety-seventh',
    '98e': 'ninety-eighth',
    '99e': 'ninety-ninth'
}

NUM_DICT_2 = {
    '1': 'first',
    '2': 'second',
    '3': 'third',
    '4': 'fourth',
    '5': 'fifth',
    '6': 'sixth',
    '7': 'seventh',
    '8': 'eighth',
    '9': 'ninth',
    '10': 'tenth',
    '11': 'eleventh',
    '12': 'twelfth',
    '13': 'thirteenth',
    '14': 'fourteenth',
    '15': 'fifteenth',
    '16': 'sixteenth',
    '17': 'seventeenth',
    '18': 'eighteenth',
    '19': 'nineteenth',
    '20': 'twentieth',
    '21': 'twenty-first',
    '22': 'twenty-second',
    '23': 'twenty-third',
    '24': 'twenty-fourth',
    '25': 'twenty-fifth',
    '26': 'twenty-sixth',
    '27': 'twenty-seventh',
    '28': 'twenty-eighth',
    '29': 'twenty-ninth',
    '30': 'thirtieth',
    '31': 'thirty-first',
    '32': 'thirty-second',
    '33': 'thirty-third',
    '34': 'thirty-fourth',
    '35': 'thirty-fifth',
    '36': 'thirty-sixth',
    '37': 'thirty-seventh',
    '38': 'thirty-eighth',
    '39': 'thirty-ninth',
    '40': 'fortieth',
    '41': 'forty-first',
    '42': 'forty-second',
    '43': 'forty-third',
    '44': 'forty-fourth',
    '45': 'forty-fifth',
    '46': 'forty-sixth',
    '47': 'forty-seventh',
    '48': 'forty-eighth',
    '49': 'forty-ninth',
    '50': 'fiftieth',
    '51': 'fifty-first',
    '52': 'fifty-second',
    '53': 'fifty-third',
    '54': 'fifty-fourth',
    '55': 'fifty-fifth',
    '56': 'fifty-sixth',
    '57': 'fifty-seventh',
    '58': 'fifty-eighth',
    '59': 'fifty-ninth',
    '60': 'sixtieth',
    '61': 'sixty-first',
    '62': 'sixty-second',
    '63': 'sixty-third',
    '64': 'sixty-fourth',
    '65': 'sixty-fifth',
    '66': 'sixty-sixth',
    '67': 'sixty-seventh',
    '68': 'sixty-eighth',
    '69': 'sixty-ninth',
    '70': 'seventieth',
    '71': 'seventy-first',
    '72': 'seventy-second',
    '73': 'seventy-third',
    '74': 'seventy-fourth',
    '75': 'seventy-fifth',
    '76': 'seventy-sixth',
    '77': 'seventy-seventh',
    '78': 'seventy-eighth',
    '79': 'seventy-ninth',
    '80': 'eightieth',
    '81': 'eighty-first',
    '82': 'eighty-second',
    '83': 'eighty-third',
    '84': 'eighty-fourth',
    '85': 'eighty-fifth',
    '86': 'eighty-sixth',
    '87': 'eighty-seventh',
    '88': 'eighty-eighth',
    '89': 'eighty-ninth',
    '90': 'ninetieth',
    '91': 'ninety-first',
    '92': 'ninety-second',
    '93': 'ninety-third',
    '94': 'ninety-fourth',
    '95': 'ninety-fifth',
    '96': 'ninety-sixth',
    '97': 'ninety-seventh',
    '98': 'ninety-eighth',
    '99': 'ninety-ninth'
}

BAD_LIST_1 = [
    r'^\d+st',
    r'^\d+nd',
    r'^\d+rd',
    r'^\d+th',
    r'^\d+e',
    r'^\d+re'
]

BAD_LIST_2 = [
    r'^\d+ st',
    r'^\d+ av',
    r'^\d+ ave',
    r'^\d+ rue',
    r'^\d+\b'
]


def number_to_text(input_string):
    output_string = input_string
    check = re.match('|'.join(BAD_LIST_1), input_string)
    if check:
        expr = input_string.split()[0]
        if expr in NUM_DICT_1.keys():
            output_string = output_string.replace(expr, NUM_DICT_1[expr])
    else:
        check2 = re.match('|'.join(BAD_LIST_2), input_string)
        if check2:
            expr = input_string.split()[0]
            if expr in NUM_DICT_2.keys():
                output_string = output_string.replace(expr, NUM_DICT_2[expr])

    return output_string


# reverse dictionary to turn words to numbers
text_dict = {v: k for k, v in NUM_DICT_2.items()}
BAD_LIST_3 = [
    r'^\d+st$',
    r'^\d+st st$',
    r'^\d+st ave$',
    r'^\d+st av$',
    r'^\d+nd$',
    r'^\d+nd$ st',
    r'^\d+nd$ ave',
    r'^\d+nd av$',
    r'^\d+rd$',
    r'^\d+rd st$',
    r'^\d+rd ave$',
    r'^\d+rd av$',
    r'^\d+th$',
    r'^\d+th st$',
    r'^\d+th ave$',
    r'^\d+th av$',
    r'^\d+e$',
    r'^\d+re$'
]

BAD_LIST_4 = [
    r'^\d+ st$',
    r'^\d+ av$',
    r'^\d+ ave$',
    r'^\d+ rue$',
    r'^\d+\b$'
]

def texttonumber(input_string):
    output_string = input_string
    check = re.match('|'.join(BAD_LIST_3), input_string)

    # print(check)
    if check:
        output_string = re.match(re.compile(r'\d+'), input_string)[0]
        
    else:
        check2 = re.match('|'.join(BAD_LIST_4), input_string)
        if check2:
            output_string = re.match(re.compile(r'\d+'), input_string)[0]
        else: 
            
            if input_string in text_dict.keys():
                output_string = input_string.replace(input_string, text_dict[input_string])
    return output_string
