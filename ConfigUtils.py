#!/usr/bin/env python3

#Function simpleParseConfig: Reads Config Files
#Input: String
#Output: Dict
def simpleParseConfig(FILE):
    #Read the File
    f = open(FILE,'r')
    D = f.read().replace('\t','').replace(' ','').split('\n')
    f.close()

    #The Output Dict
    RESULTS = {}

    for i in D:
        if ('#' not in i) and (i != ''):
            N,V = i.split('=')
            if N in list(RESULTS.keys()):
                O = RESULTS[N]
                if type(O) == list:
                    RESULTS[N].append(V)
                else:
                    RESULTS[N] = [O,V]
            else:
                RESULTS[N] = V

    return RESULTS

#Function complexParseConfig: Reads Config Files, allowing for grouped and duplicate values
#Input: String
#Output: Dict
def complexParseConfig(FILE):
    #Read the File
    f = open(FILE,'r')
    D = f.read().replace('\t','').replace(' ','').split('\n')
    f.close()

    #The Output Dict
    RESULTS = {}
    #This Flag detects if the variables are grouped
    KY = False

    for i in D:
        if ('#' not in i) and (i != ''):
            if 'START' in i:
                KY = i.split(':')[1]
                RESULTS[KY] = {}
            elif 'END' in i:
                KY = False
            
            else:
                N,V = i.split('=')
                #IF Group Flag
                if KY:
                    if N in list(RESULTS[KY].keys()):
                        O = RESULTS[KY][N]
                        if type(O) == list:
                            RESULTS[KY][N].append(V)
                        else:
                            RESULTS[KY][N] = [O,V]
                    else:
                        RESULTS[KY][N] = V
                else:
                    if N in list(RESULTS.keys()):
                        O = RESULTS[N]
                        if type(O) == list:
                            RESULTS[N].append(V)
                        else:
                            RESULTS[N] = [O,V]
                    else:
                        RESULTS[N] = V

    return RESULTS