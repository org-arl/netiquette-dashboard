import nq
import re, sys
import datetime

quanta = 5
hours = 24
blksize = 10.0

data = nq.read_logs(
    regex=r'Netiquette.*:: (Rx.*)$',
    max_age=hours*3600,
    process=lambda t,x: (t, x[0])
)

if len(data) == 0:
    sys.exit()

cdata = [[], [], []]
db = {}

def median(l):
    if l is None or len(l) == 0: return None
    half = len(l)//2
    l.sort()
    return (l[half-1]+l[half])/2.0 if len(l)%2 == 1 else l[half]

def type(s):
    if s == 'CONTROL': return 0
    if s == 'DATA': return 1
    if s == '#3': return 2
    return None

def reset():
    db['count'] = [0, 0, 0]
    db['detector'] = [[], [], []]
    db['ber'] = [[], []]
    db['rssi'] = [[], [], []]

def process(s):
    m = re.match(r'RxFrameStartNtf.*type:([#A-Z0-9]+) .* detector:(0.\d+)', s)
    if m:
        n = type(m.group(1))
        if n is None: return
        if db['count'][n] < blksize: db['count'][n] = db['count'][n] + 1
        db['detector'][n].append(float(m.group(2)))
        return
    m = re.match(r'RxFrameNtf.*type:([#A-Z0-9]+) .* ber:(\d+)/(\d+)', s)
    if m:
        n = type(m.group(1))
        if n is None: return
        db['ber'][n].append(float(m.group(2))/float(m.group(3)))
        m = re.search(r' rssi:(\-?\d+\.?\d*)', s)
        if m: db['rssi'][n].append(float(m.group(1)))
        return
    m = re.match(r'RxBasebandSignalNtf.*rssi:(\-?\d+\.?\d*) .* preamble:3', s)
    if m:
        db['rssi'][2].append(float(m.group(1)))
        return

def summarize(label):
    d = (label,) + (db['count'][0]/blksize, db['count'][1]/blksize, db['count'][2]/blksize) + \
        (median(db['detector'][0]), median(db['detector'][1]), median(db['detector'][2])) + \
        (median(db['ber'][0]), median(db['ber'][1])) + \
        (median(db['rssi'][0]), median(db['rssi'][1]), median(db['rssi'][2]))
    return d

t = data[0][0]
t = datetime.datetime(t.year, t.month, t.day, t.hour, quanta*(t.minute//quanta), 0, 0, t.tzinfo)
dt = datetime.timedelta(minutes=quanta)
k = 0
while k < len(data) and data[k][0] < t:
    k = k + 1
for j in range(int(60.0/quanta*hours)):
    ot = t
    t = t + dt
    reset()
    while k < len(data) and data[k][0] < t:
        process(data[k][1])
        k = k + 1
    cdata[(ot.minute//quanta)%3].append(summarize("%02d"%(ot.hour)))

nq.export_json(cdata[0], cols=(1,4,7),   filename='data/commsA1.json')
nq.export_json(cdata[1], cols=(1,4,7),   filename='data/commsB1.json')
nq.export_json(cdata[2], cols=(1,4,7),   filename='data/commsC1.json')
nq.export_json(cdata[0], cols=(2,5,8),   filename='data/commsA2.json')
nq.export_json(cdata[1], cols=(2,5,8),   filename='data/commsB2.json')
nq.export_json(cdata[2], cols=(2,5,8),   filename='data/commsC2.json')
nq.export_json(cdata[0], cols=(3,6),     filename='data/commsA3.json')
nq.export_json(cdata[1], cols=(3,6),     filename='data/commsB3.json')
nq.export_json(cdata[2], cols=(3,6),     filename='data/commsC3.json')
nq.export_json(cdata[0], cols=(9,10,11), filename='data/rssiA.json')
nq.export_json(cdata[1], cols=(9,10,11), filename='data/rssiB.json')
nq.export_json(cdata[2], cols=(9,10,11), filename='data/rssiC.json')
