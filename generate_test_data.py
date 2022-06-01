import random
from datetime import datetime, timedelta
import json
import requests
import os
from urllib import parse
import base64
import uuid

number_of_samples=150
id=uuid.uuid4()
filename=f'{id}_data.json'
labelfile=f'{id}_data.labeling.json'
data=[]
labeling=[]
with open(filename,'w+') as test_file:
    for i in range(number_of_samples):
        random_speed= round(random.uniform(0,10), 2)
        random_temp= round(random.uniform(-10,50), 2)
        random_coords = [round(random.uniform(-180,180),6), round(random.uniform(-90, 90),6)]

        min_year=1970
        max_year=datetime.now().year
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        random_ts= int((start + (end - start) * random.random()).timestamp()*1000)

        for i in ['camera','lidar','radar']:
            url = 'https://picsum.photos/1920/1080'
            response = requests.get(url)
            extension = os.path.splitext(parse.urlsplit(response.url).path)[-1]
            image_name = f'{i}{extension}'
            path = f'{image_name}'
            with open(path, mode='wb') as f:
                f.write(response.content)
            if i=='camera':
                with open(image_name, "rb") as image_file:
                    camera_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            elif i=='lidar':
                with open(image_name, "rb") as image_file:
                    lidar_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                with open(image_name, "rb") as image_file:
                    radar_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            os.remove(image_name)

        data.extend(
        [{"attribute":"speed","metric":random_speed,"unit":"m/s","timestamp":random_ts},
        {"attribute":"image","type":"camera","metric":f"{camera_b64}","timestamp":random_ts},
        {"attribute":"image","type":"lidar","metric":f"{lidar_b64}","timestamp":random_ts},
        {"attribute":"image","type":"radar","metric":f"{radar_b64}","timestamp":random_ts},
        {"attribute":"temperature","metric":random_temp,"unit":"centigrade","timestamp":random_ts},
        {"attribute":"gps","metric":random_coords,"timestamp":random_ts}])

        for i in range(random.choice(list(range(4)))):
            label_list=['car', 'truck', 'road sign', 'traffic sign', 'pedestrian', 'animal']
            random_label=random.choice(label_list)
            type_list=['camera','lidar','radar']
            random_type=random.choice(type_list)
            labeling.append({"entity":f"{random_label}","caught_on":f"{random_type}","timestamp":random_ts})

    json.dump(data, test_file)

with open(labelfile,'w+') as labelfile:
    json.dump(labeling, labelfile)

print(os.path.getsize(filename))

