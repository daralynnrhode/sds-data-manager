import json
import urllib.parse
import boto3
import logging 

s3 = boto3.client('s3')

def _load_allowed_filenames():
    # Rather than storing the configuration locally, we should store the configuration somewhere where things can be changed on the fly.  
    # For example, a dynamodb table or a section in opensearch
    with open("config.json") as f:
        data = json.load(f)
    return data

def _check_for_matching_filetype(pattern, filename):
    # This function loads in the 
    split_filename = filename.replace("_", ".").split(".")

    if len(split_filename) != len(pattern):
        return None
    
    i = 0
    file_dictionary = {}
    for field in pattern:
        if pattern[field] == '*':
            file_dictionary[field] = split_filename[i]
        elif pattern[field] == split_filename[i]:
            file_dictionary[field] == split_filename[i]
        else:
            return None
        i += 1
    
    return file_dictionary

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    # Retrieve a list of allowed file types
    filetypes = _load_allowed_filenames()
    logger.info("Allowed file types: " + filetypes)

    # We're only expecting one record, but for some reason the Records are a list object
    for record in event['Records']:
        
        # Retrieve the Object name
        logger.info(f'Record Received: {record}')
        bucket = record['s3']['bucket']['name']
        filename = record['s3']['object']['key']

        logger.info(f"Attempting to insert {filename} into database")

        # Look for matching file types in the configuration
        for filetype in filetypes:
            metadata = _check_for_matching_filetype(filetype['pattern'], filename)
            if metadata is not None:
                break
        
        # Rather than returning the metadata, we should insert it into the DB
        return metadata


    
