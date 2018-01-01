#!/usr/bin/env python3

import ceo, event_agent, response_agent, monitor_agent, speaker_agent, analysis_agent
import testscript

exec_func = {'egen': event_agent.egen,
             'eand': event_agent.eand,
             'eor' : event_agent.eand,
             'enot': event_agent.eand,

             'moni': monitor_agent.moni,

             'notf': speaker_agent.notf,
             'cfrm': speaker_agent.cfrm,

             'sell': response_agent.sell,
             'buy' : response_agent.buy}

sj = ceo.CEO (testscript.script, exec_func)
sj.run ()

sj.idle ()

