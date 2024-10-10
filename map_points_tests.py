from routes import map_point,map_points
import pandas as pd
import time

locations = list(pd.read_csv('locations.csv').itertuples())
print(f'mapping {len(locations)} locations')

locations
mapped = []
print(len(locations))
start_time = time.time()
for idx,location in enumerate(locations):
    facility = [location.id]
    mapping = map_point(location.location_lon, location.location_lat)

    mapped.append(facility + mapping)

    if (idx +1) % 20 == 0:
        print(f"\r{idx+1} of {len(locations)}",end='')

print("\n",time.time()-start_time)
results = pd.DataFrame(mapped).to_csv('mapped_locations.csv')
# placetypes = [map_point(location.location_lon,location.location_lat) for location in locations]
# print('done')