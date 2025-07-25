import glob
import pandas as pd 
import xml.etree.ElementTree as ET
from datetime import datetime

# Writting the log file and target file names
log_file = "log_file.txt"
target_file = "transformed_data.csv"

# Extract data from csv
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

# Extract data from json
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process)
    return dataframe

# Extract data from xml
def extract_from_xml(file_to_process): 
    rows = []
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        rows.append({"name": name, "height": height, "weight": weight})
    dataframe = pd.DataFrame(rows)
    return dataframe

# Identify which function to call based on the type of file
def extract():
    extracted_data = pd.DataFrame(columns=['name','height','weight'])
    for csvfile in glob.glob("*.csv"):
        if csvfile != target_file:
            new_data = extract_from_csv(csvfile)
            if extracted_data.empty:
                extracted_data = new_data
            else:
                extracted_data = pd.concat([extracted_data, new_data], ignore_index=True)
    # Repeat similar logic for JSON and XML
    for jsonfile in glob.glob("*.json"):
        new_data = extract_from_json(jsonfile)
        if extracted_data.empty:
            extracted_data = new_data
        else:
            extracted_data = pd.concat([extracted_data, new_data], ignore_index=True)
    for xmlfile in glob.glob("*.xml"):
        new_data = extract_from_xml(xmlfile)
        if extracted_data.empty:
            extracted_data = new_data
        else:
            extracted_data = pd.concat([extracted_data, new_data], ignore_index=True)
    return extracted_data

# Convert the height from inches to meters and weight from pounds to kilograms
def transform(data): 
    '''Convert inches to meters and round off to two decimals 
    1 inch is 0.0254 meters '''
    data['height'] = round(data.height * 0.0254,2) 
 
    '''Convert pounds to kilograms and round off to two decimals 
    1 pound is 0.45359237 kilograms '''
    data['weight'] = round(data.weight * 0.45359237,2) 
    
    return data

# Loading and Logging 

def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file) 
    
# Logging the ETL process
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a", encoding="utf-8") as f: 
        f.write(timestamp + ',' + message + '\n') 

# Testing the ETL process
# Log the initialization of the ETL process 
log_progress("ETL Job Started")

# Log the beginning of the Extraction process 
log_progress("Extract phase Started")
extracted_data = extract() 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
 
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 
