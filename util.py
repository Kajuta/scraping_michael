from lib import json , re

def loggingScrap(dictObj) -> None:
    if isinstance(dictObj,dict):
        logmsg = json.dumps(dictObj)
        with open('scrapingLog.txt','a') as f:
            f.write(logmsg + '\n')
            
    else:
        return 0

def textInstr(text,instr):
    ptn = re.compile(instr)
    res = ptn.match(text)
    ret = {
        'bool':(res != None),
        'result':res
    }
    return ret