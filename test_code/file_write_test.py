import json
import csv

test_number = 1


#Create 3 frames.csv and 3 meta.json files
for i in range(0,3,1):

    #Create and Write meta.json files
    metadata = {
    "boxModelNumber": str(i),
    "boxSerialNumber": "0000" + str(i),
    "recordStart": "2024-01-01T12:00:00.000Z",
    "recordEnd": "2024-01-01T12:00:00.500Z",
    "fps": 10
    }

    json_object = json.dumps(metadata, indent=4)

    with open("../data/metadata/meta" + str(test_number) + ".json","w") as outfile:
        outfile.write(json_object)
    
    #Create and Write frames.csv
    filename = "../data/framedata/frames" + str(test_number) + ".csv"
    with open(filename, "w", newline = '') as outfile:
        writer = csv.writer(outfile)
        field = ["frameIndex", "timestamp", "latitude", "longitude", "heading", "groundHeightMeters"]
        writer.writerow(field)
        writer.writerow(["0", "2024-01-01T12:00:00.00Z", "0.0", "0.0", str(test_number), "3.048"])

    test_number += 1


