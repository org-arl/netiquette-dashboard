import nq

data = nq.read_logs(
    regex=r'DATA\|Data\|(.*)$',
    min_gap=60,
    process=lambda t,x: ('%02d'%(t.hour),)+nq.csv(x, cols=(1,2,4,8,10,12))
)

nq.export_json(data, cols=(1,), filename='data/weather_atm.json')
nq.export_json(data, cols=(2,), filename='data/weather_temp.json')
nq.export_json(data, cols=(3,), filename='data/weather_rh.json')
nq.export_json(data, cols=(4,), filename='data/weather_wind_dir.json')
nq.export_json(data, cols=(5,), filename='data/weather_wind_speed.json')
nq.export_json(data, cols=(5,), filename='data/weather_light.json')
