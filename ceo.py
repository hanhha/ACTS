#/usr/bin/env python3

from queue import Queue 
from threading import Thread, Event
import copy
import signal

def norm (param):
    if type(param) is str:
        return param.strip().lower()
    else:
        return param

confInst = {'tick':'tick', 'fltr':'filter'}
trigInst = {'pcmp':'price compare', 'ptrnd': 'price trend'}
evntInst = {'eand':'and', 'eor':'or', 'enot':'not', 'egen': 'generate'}
notfInst = {'notf':'notify', 'cfrm':'confirm'}
trdeInst = {'sell':'sell', 'buy':'buy'}
moniInst = {'moni':'monitor'}
tmp = {**confInst, **trigInst, **evntInst, **notfInst, **trdeInst, **moniInst}
InstOpc = dict (zip (tmp.values(), tmp.keys()))

class CEO ():
    def __init__ (self, script, executives):
        self._script = script.copy ()
        self._executives = copy.deepcopy (executives)
        self.tick = 300
        self.filter = 3
        self.eventQueues = dict ()
        self.execThreads = list () 
        self.allStop = Event ()

    def run (self):
        self.eventQueues, processes_list = self.parse_script_commands (self._script)
        for process in processes_list:
            outQ = self.eventQueues [process[2]] if process[2] is not None else None
            if type(process[1]) is dict:
                inpQlist = list()
                for inpQ, qid in process[1].items():
                    inpQlist.append (self.eventQueues[inpQ][qid])
                if len(inpQlist) == 1:
                    inpQlist = inpQlist [0]

                self.execThreads.append (Thread (target = self._executives [process[0]], args = (inpQlist, outQ, process[3], self.allStop, )))
            else:
                self.execThreads.append (Thread (target = self._executives [process[0]], args = (process[1], outQ, process[3], self.allStop, )))
            self.execThreads[-1].daemon = True

        for t in self.execThreads:
            t.start ()

    def stop (self, signo, _frame):
        print ("Interrupted by %d, shuting down" % signo)
        self.allStop.set ()

    def idle (self):
        for sig in ('INT', 'TERM', 'HUP'):
            signal.signal (getattr(signal, 'SIG' + sig), self.stop)

        for t in self.execThreads:
            t.join ()
        print ('All workers stopped.')
        for q in [item for qlist in self.eventQueues.values() for item in qlist]:
            q.join ()
        print ('All to-do cleaned.')
        self.allStop.clear ()

    def parse_script_commands (self, command_list):
        retQueues = dict()
        retProcesses = list()

        for inst in command_list:
            inst = list(map (norm, inst))
            opc = InstOpc[inst [0]]

            if opc in trigInst.keys():
                outEvt = inst [-1]
                if outEvt not in retQueues.keys():
                    retQueues [outEvt] = list()

                inpEvt = inst [1]
                if inpEvt not in retQueues.keys():
                    retQueues [inpEvt] = list()
                qid = len(retQueues[inpEvt])
                retQueues[inpEvt].append (Queue(maxsize=1))

                retProcesses.append ([opc, {inpEvt:qid}, outEvt, inst[2:-1]])

            elif opc in moniInst.keys():
                outEvt = inst [-1]
                if outEvt not in retQueues.keys():
                    retQueues [outEvt] = list()

                inpEvt = inst [1]
                if inpEvt not in retQueues.keys():
                    retQueues [inpEvt] = list()
                qid = len(retQueues[inpEvt])
                retQueues[inpEvt].append (Queue(maxsize=1))

                retProcesses.append ([opc, {inpEvt:qid}, outEvt, inst[2:-1]])

            elif opc in evntInst.keys():
                outEvt = inst [-1]
                if outEvt not in retQueues.keys():
                    retQueues [outEvt] = list()
                
                inpEvt = None if opc is 'egen' else {ievt:0 for ievt in inst [1:-1]}
                if inpEvt is not None:
                    for ievt in inpEvt.keys():
                        if ievt not in retQueues.keys():
                            retQueues [ievt] = list()
                        qid = len(retQueues[ievt])
                        retQueues[ievt].append (Queue(maxsize=1))
                        inpEvt [ievt] = qid

                retProcesses.append ([opc, inpEvt, outEvt, self.tick])

            elif opc in notfInst.keys():
                if opc is notfInst['cfrm']:
                    outEvt = inst [-1]
                    if outEvt not in retQueues.keys():
                        retQueues [outEvt] = list()
                else:
                    outEvt = None

                inpEvt = inst [1]
                if inpEvt not in retQueues.keys():
                    retQueues [inpEvt] = list()
                qid = len(retQueues[inpEvt])
                retQueues[inpEvt].append (Queue(maxsize=1))

                retProcesses.append ([opc, {inpEvt:qid}, outEvt, inst[2:-1]])

            elif opc in trdeInst.keys():
                if len(inst) == 6:
                    outEvt = inst [-1]
                    if outEvt not in retQueues.keys():
                        retQueues [outEvt] = list()

                inpEvt = inst [1]
                if inpEvt not in retQueues.keys():
                    retQueues [inpEvt] = list()
                qid = len(retQueues[inpEvt])
                retQueues[inpEvt].append (Queue(maxsize=1))

                retProcesses.append ([opc, {inpEvt:qid}, outEvt, inst[2:-1]])

            elif opc in confInst.keys():
                if opc is confInst['tick']:
                    self.tick = inst [1]
                elif opc is confInst['fltr']:
                    self.filter = inst [1]

            else:
                print ("Invalid instruction:")
                print (inst)
                break
        return retQueues, retProcesses
