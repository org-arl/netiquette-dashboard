from __future__ import print_function
import sys, re
import time, pytz, datetime
import json

def read_logs(max_age=86400, min_gap=0, regex=None, process=None, epoch=False):
    t0 = time.time()
    last = 0
    data = []
    for line in sys.stdin:
        m = re.match(r'(\d+)\|', line)
        if m:
            t = int(m.group(1)[:-3]) if len(m.group(1)) > 10 else int(m.group(1))
            age = t0-t
            if age <= max_age and t-last >= min_gap:
                if regex is not None:
                    m1 = re.search(regex, line)
                if regex is None or m1:
                    dts = t if epoch else datetime.datetime.fromtimestamp(t, pytz.timezone('Asia/Singapore'))
                    data1 = m1.groups() if m1 else None
                    data1 = process(dts, data1) if process else (dts,) + data1
                    if data1 is not None:
                        data.append(data1)
                    last = t
    return data

def export_json(data, cols=None, trim_labels=True, filename=None):
    if data is None or len(data) == 0:
        s = '{}'
    else:
        labels = [_[0] for _ in data]
        if trim_labels:
            last = labels[0]
            for j in range(1, len(labels)):
                if last == labels[j]:
                    labels[j] = ''
                else:
                    last = labels[j]
        if len(data[0]) == 2:
            series = [_[1] for _ in data]
        else:
            series = [[_[j] for _ in data] for j in (cols if cols else range(1,len(data[0])))]
        s = json.dumps({'labels': labels, 'series': series})
    if filename is not None:
        with open(filename, 'w') as f:
            print(s, file=f)
    return s

def csv(s, dtype=float, cols=None):
    if isinstance(s, (list,tuple)):
        s = s[0]
    x = s.split(',')
    if cols:
        x = [x[j] for j in cols]
    if dtype:
        x = [dtype(_) for _ in x]
    return tuple(x)
