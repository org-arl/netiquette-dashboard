import nq

data = nq.read_logs(
    regex=r'DATA\|data\|(.*)$',
    min_gap=60,
    process=lambda t,x: ('%02d'%(t.hour),)+nq.csv(x, cols=(2,4,9,11))
)

nq.export_json(data, cols=(1,2), filename='data/voltage.json')
nq.export_json(data, cols=(3,4), filename='data/power.json')
