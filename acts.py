#!/usr/bin/env python3

import ceo, event_agent, response_agent, monitor_agent, speaker_agent, analysis_agent, acts_bot
import tradescript

exec_func = {'egen': event_agent.egen,
             'eand': event_agent.eand,
             'eor' : event_agent.eor,

             'moni': monitor_agent.moni,

             'notf': speaker_agent.notf,
             'cfrm': speaker_agent.cfrm,

             'sell': response_agent.sell,
             'buy' : response_agent.buy}

print ('Waiting for user start the chat bot ... ')
while not speaker_agent.workable ():
	pass

sj = ceo.CEO (tradescript.script, exec_func)
sj.run ()
print ('System is running ...')

sj.idle ()
speaker_agent.stop()

