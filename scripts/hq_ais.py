from __future__ import print_function
import math, sys, json, datetime, pytz
import ais
import nq

def interesting(lon1, lat1):
    if lat1 > 1.218858:
        return False
    R = 6371.0
    lat2 = 1.217002
    lon2 = 103.854209
    x = (lon2-lon1)*math.pi/180 * math.cos(0.5*(lat2+lat1)*math.pi/180)
    y = (lat2-lat1)*math.pi/180
    d = R * math.sqrt(x*x + y*y)
    return d < 3

def decode(s1, s2):
    try:
        msg = ais.decode(s1, int(s2[0]))
        if 'mmsi' in msg and 'x' in msg and 'y' in msg and msg['mmsi']:
            return (str(msg['mmsi']), msg['x'], msg['y'])
    except ais.DecodeError as e:
        pass
    return None

data = nq.read_logs(
    regex=r'DATA\|Data\|(!AIVDM.*)$',
    epoch=True,
    process=lambda t,x: (t,)+tuple((x[0].split(','))[5:])
)

if data is None or len(data) == 0:
    sys.exit()

history = {}
tracks = {}
counts = []
last = data[0][0]
for d1 in data:
    dd = decode(d1[1], d1[2])
    if dd is not None and interesting(dd[1], dd[2]):
        history[dd[0]] = d1[0]
        if dd[0] in tracks:
            tracks[dd[0]].append(dd[1:])
        else:
            tracks[dd[0]] = [dd[1:]]
        if d1[0]-last > 600:
            last = d1[0]
            h1 = [k for k,v in history.iteritems() if v > d1[0]-3600]
            dts = datetime.datetime.fromtimestamp(d1[0], pytz.timezone('Asia/Singapore'))
            counts.append(['%02d'%(dts.hour,), len(h1)])

nq.export_json(counts, filename='data/ais.json')
with open('data/aisTracks.json', 'w') as f:
    print(json.dumps(tracks), file=f)
