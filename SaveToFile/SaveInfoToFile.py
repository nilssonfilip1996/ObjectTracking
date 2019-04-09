import csv
import time

# resource: https://realpython.com/python-csv/#parsing-csv-files-with-pythons-built-in-csv-library
    
with open('game_tracker_file.csv', mode='a') as tracker_file:
    tracker_writer = csv.writer(tracker_file, delimiter=',')
    
    time = time.strftime('%Y-%m-%d %H:%M:%S%z (%Z)')
    tracker_writer.writerow([time, 'Aron Polner', 'Accounting', 'November'])
    tracker_writer.writerow([time, 'Filip Nilsson', 'IT', 'March'])