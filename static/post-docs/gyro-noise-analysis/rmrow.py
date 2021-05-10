
# import csv
import csv
  
# open input CSV file as source
# open output CSV file as result
with open("accel-gyro-data.csv", "r") as source:
    reader = csv.reader(source)
      
    with open("gyrodata_100hz_6hrs.csv", newline='', mode='w') as result:
        writer = csv.writer(result)
        for r in reader:
            
            # Use CSV Index to remove a column from CSV
            writer.writerow((r[3], r[4], r[5]))
