#!/usr/bin/env python3

def notf (inpQ, outQ, params, Stop):
    if params[0] == 'rem':
        fix_str = True
        info_str = params[1]
    else:
        fix_str = False

    while not Stop.is_set ():
        if not inpQ.empty():
            info = inpQ.get (block = False)
            if fix_str:
                #TODO: notf
                print (info_str)
            else:
                if type(info) is tuple:
                    if info[0] is True:
                        #TODO: notf
                        print (info[1][params[0].upper()])
                    else:
                        #TODO: notf
                        print ("Could not get data")
                        print (info[1])
                else:
                    if info is True:
                        #TODO: notf
                        print (param[0])
            inpQ.task_done ()

def cfrm (inptQ, outQ, params, Stop):
    while not Stop.is_set ():
        if not inpQ.empty():
            tmp = inpQ.get (block = False)
            for q in outQ:
                q.put (tmp, block = True)
            print ('cfrm takes place ' + tmp)
            #TODO: cfrm
            inpQ.task_done ()

