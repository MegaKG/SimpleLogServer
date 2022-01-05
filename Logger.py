#!/usr/bin/env python3
import datetime
import os
import sys

#class logger: - Handles logs into logfile
class logger:
    #Method Initialise: Set Up the Class
    #Input: String
    #Ouput: None
    def __init__(self,filename):
        print("Init Logger")
        if os.path.exists(filename):
            f = open(filename,'a')
            f.write("\n\nStart Program " + str(datetime.datetime.now()) + "\n")
            f.close()
        else:
            f = open(filename,'a')
            f.write("Start Program " + str(datetime.datetime.now()) + "\n")
            f.close()
        
        self.filename = filename

    #Method Log: Logs a value
    #Input: ANY
    #Output: None
    def log(self,Input):
        f = open(self.filename,'a')
        f.write(str(datetime.datetime.now()) + ' ' + str(Input) + '\n')
        f.close()
        sys.stdout.write(str(Input) + '\n')
        sys.stdout.flush()
        

