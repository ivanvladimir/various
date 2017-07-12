#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
from tinydb import TinyDB, Query
import os
import json

# Función principal (interfaz con línea de comandos)
if __name__ == '__main__':
    p = argparse.ArgumentParser("conversations")
    p.add_argument("DIR",
            help="Dir with json conversations")
    p.add_argument("-json", default="out.json",
            action="store", dest="jsonfile",
            help="Json file with all conversations [out.json]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    opts = p.parse_args()

    conversationfiles = [os.path.join(d, x)
                for d, dirs, files in os.walk(opts.DIR)
                for x in files if x.endswith(".json")]

    nconversations=0
    ntotalturnos=0
    jconv=[]
    for jsonfile in conversationfiles:
        db = TinyDB(jsonfile)
        for item in db.all():
            if len(item['conversations'])<=2:
                continue
            for conversation in item['conversations']:
                jconv.append([])
                for nturn,turn in enumerate(conversation):
                    if len(turn['msg'])==0 or len(turn['ans'])==0:
                        continue
                    print("TURNO {0: >3}: {1}".format(nturn,turn['msg']))
                    print("         : {0}".format(turn['ans']))
                    jconv[-1].append((turn['msg'],turn['ans']))
                    ntotalturnos+=1
                print("")
                nconversations+=1


    print("Total systems      ",len(conversationfiles))
    print("Total conversations",nconversations)
    print("Total turnos       ",ntotalturnos)

    with open(opts.jsonfile, 'w', encoding="utf8") as outfile:
        json.dump(jconv, outfile, sort_keys=True, indent=4, ensure_ascii=False)




   
