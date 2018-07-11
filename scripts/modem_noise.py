import nq

data = nq.read_logs(
    regex=r'NOISE (\-?\d+\.\d+)',
    process=lambda t,x: ('%02d'%(t.hour), float(x[0]))
)

nq.export_json(data, cols=(1,2), filename='data/noise.json')
