#!/usr/bin/python=python3.6
# -*- coding: utf-8 -*-

import re, csv, os
def log_speech(corpusfile):
    with open(corpusfile,"r") as f, open("speech_"+corpusfile[:-3]+"csv","w") as w:
        wwriter = csv.writer(w, delimiter='\t')
        line = f.readline()
        while line:
            if len(line.split(":"))>=4:
                line       = line.rstrip()
                elements   = line.split(":")
                num        = elements[0]
                speech     = elements[-2]
                charact    = elements[-1]
                # print(charact)
                for sp in speech.split("。"):
                    if sp!='':
                        row = ["timestamp",num,sp,charact]
                        wwriter.writerow(row)
            line = f.readline()


if __name__ == '__main__':
    dossier_list = os.listdir(".")

    # for d in dossier_list:
    #     if d[0]=="r" and d[-3:]=="txt":
    #         log_speech(d)
    # log_speech("rS3E203.txt")
