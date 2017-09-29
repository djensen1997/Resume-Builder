#!/usr/bin/python3
"""
###############################################################################
#   Resume Builder (Python Portion)
#
#   Purpose: an automated way to generate a resume from scratch or an xml file
#
#   Usage: python3 build.py <dat save file>
#
#   Possible Flags:
#
###############################################################################
"""



import sys
import os


save = None
savef = None
items = []
STATE_CATAGORY = 0
STATE_ITEM = 1
STATE_DESCRIPTION = 2
STATE_HEADER = 3
STATE_SKILLS = 4
STATE_TERM = 5
MODE_EDIT = 0
MODE_NEW = 1

def parsedat():
    """
        Method to parse the dat file
    """
    line = savef.readline()
    item = 0
    curr = []
    while line != "":
        #print (line)
        if line == '\n':
            continue
        else:
            line = line.strip()
            if len(line) == 0:
                continue
            if item == 0:#not parsing an item
                try:
                    #print("making a dict for {}".format(line))
                    parts = line.split(' = ')
                    if curr != []:
                        items.append(curr)
                    curr = [parts[0], {}]
                    item = 1
                except:
                    print( 'Illegal Format Exception')
            else:
                if line == "}":
                    items.append(curr)
                    curr = []
                    item = 0
                else:
                    try:
                        #print('adding {} to the dict'.format(line))
                        parts = line.split(' = ')
                        if parts[1] == '{':
                            pass
                        else:
                            curr[1][parts[0]] = parts[1]
                    except:
                        print ('Illegal Format Exception')
        line = savef.readline()

def inputdat():
    """
        The statemachine for inputting data to the resume
    """
    item = []
    prompt = ""
    output = ""
    mode = MODE_NEW
    if len(items) > 0:
        for i in range(0, len(items)):
            item = items[i]
            if item[0] == "contact":
                item = items[i]
                prompt = "Edit Contact Info? (y or n)  "
                mode = MODE_EDIT
        if item == []:
            prompt = "np"
            output = "Collecting Contact Info"
            mode = MODE_NEW
    state = STATE_HEADER
    while state != STATE_TERM:
        value = None
        if prompt == 'np':
            print(output)
        else:
            value = input(prompt)
        if state == STATE_HEADER:
            order = [
                "name",
                "email",
                "phone",
                "addr1",
                "addr2",
                "other",
            ]
            aorder = [
                'street addr',
                'line2',
                'city',
                'state',
                'zip',
            ]
            if mode == MODE_EDIT and value == 'y':
                #order
                #print (item)
                for i in order:
                    print("{} = {}".format(i, item[1][i]))
                    value = input("Would you like to Change This? (y or n)  ")
                    if value == 'y':
                        if i.find('addr', 0, len(i)) >= 0:
                            temp = {}
                            for j in aorder:
                                temp[j] = input('{}?  '.format(j))
                            out = ''
                            if temp['line2'] != '':
                                out = '{},<br>{},<br>'.format(temp['street addr'], temp['line2'])
                            else:
                                out = '{},<br>'.format(temp['street addr'])
                            #print (temp)
                            out += '{}, {}, {}'.format(temp['city'], temp['state'], temp['zip'])
                            item[1][i] = out
                        else:
                            item[1][i] = input("Type new value:  ")
                    else:
                        #nothing special for no
                        pass
            elif mode == MODE_NEW:
                for i in order:
                    if i.find('addr', 0, len(i)) >= 0:
                        temp = {}
                        for j in aorder:
                            temp[j] = input('{}?  '.format(j))
                        out = ''
                        if temp['line2'] != '':
                            out = '{},<br>{},<br>'.format(temp['street addr'], temp['line2'])
                        else:
                            out = '{},<br>'.format(temp['street addr'])
                        #print (temp)
                        out += '{}, {}, {}'.format(temp['city'], temp['state'], temp['zip'])
                        item[1][i] = out
                    else:
                        item[1][i] = input("{}:  ".format(i))

        elif state == STATE_CATAGORY:
            pass

        value = input("Continue? (y or n)  ")
        if value == 'n':
            state = STATE_TERM
        else:
            state = STATE_CATAGORY
            mode = MODE_NEW


def savedat():
    """
        Method to save data to the dat file
    """
    savef.seek(0, 0)
    for i in range(0, len(items)):
        item = items[i]
        savef.write('{} = {{\n'.format(item[0]))
        l = item[1].items()
        for pair in l:
            if(pair[1] == ""):
                continue
            savef.write('\t{} = {}\n'.format(pair[0], pair[1]))
        savef.write('}\n')

def main():
    """
    Main Method
    """
    global save,savef
    args = sys.argv
    if len(args) == 1:
        print ('Usage: python3 build.py <dat file>')
        sys.exit(0)
    else:
        save = args[1]
    savef = open(save, 'r+')
    savef.seek(0, 0)     #sets the cursor to the front of the doc
    parsedat()
    response = input('change data? (y or n):  ')
    if response == 'y':
        #change data
        inputdat()
    response = input('generate resume? (y or n):  ')
    if response == 'y':
        #generate resume
        pass
    savedat()
    savef.close()
    sys.exit(0)

main()
