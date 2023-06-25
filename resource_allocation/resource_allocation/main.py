import pandas as pd

from resource_allocation.resource_manager import ResourceManager
from resource_allocation.entities.surgery import Surgery

df = pd.read_csv('surgeries.csv').drop(columns = ['Unnamed: 0'])
df['procedure_id'] = range(len(df))

df['start'] = pd.to_datetime(df['start'])
df['end'] = pd.to_datetime(df['end'])

df.sort_values(by = ['start', 'end'], inplace = True)

surgeries = []
for (_, row) in df.iterrows():
    start = row['start']
    end = row['end']
    surgery_id = row['procedure_id']

    surgeries.append(Surgery(surgery_id=surgery_id, start_time=start, end_time=end))

surgeries = sorted(surgeries, key = lambda x: x.start_time)
len(surgeries)




resources_manager = ResourceManager(20, 15)
allocations = resources_manager.allocate_resources(surgeries)

print(f'{len(allocations)} {len(surgeries)}')

rows  = [(allocation.anesthesiologist.anesthesiologists_id, allocation.room.room_id,
        allocation.start_time, allocation.end_time ) for allocation in  allocations]



dd = pd.DataFrame(rows, columns = ['anesthetist_id', 'room_id', 'start_time', 'end_time'])
dd['anesthetist_id'] = dd['anesthetist_id'].apply(str)
dd['room_id'] = dd['room_id'].apply(str)

dd.to_parquet('data.parquet')


