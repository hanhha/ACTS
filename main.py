#!/usr/bin/env python3

import ceo, event_agent, response_agent, monitor_agent, speaker_agent, analysis_agent
import testscript

exec_func = {'egen': event_agent.egen,
             'moni': monitor_agent.moni,
             'notf': speaker_agent.notf}
sj = ceo.CEO (testscript.script, exec_func)
sj.run ()
try:
    while True:
        pass
except KeyboardInterrupt:
    print ("User interrupted")
sj.stop ()
sj.wait_idle ()

