import base64
import mimetypes
import os
import sys
import csv
import math
import boto3
from botocore.exceptions import ClientError
import json


config_json = json.load(open("./config.json", "r"))
config_json = config_json["isi"]
AWS_ACCESS_KEY_ID = config_json['AWS_ACCESS_ID']
AWS_SECRET_ACCESS_KEY = config_json['AWS_ACCESS_SECRET']
IMAGE_PATH = "AMT_IMAGES_CROPPED/"
S3_BUCKET = "amt-images-cropped-isi"
s3_client = boto3.client('s3', 
                        region_name="us-west-1",
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
						aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
BATCH_PATH = "AMT_BATCHES_CROPPED/"
IMAGE_PROPS = ["transaction_id","trial_id","trial_name","attack_id", "attack_id_full"]
DATA_URL_COLUMN = "url"
BATCH_SIZE = 10


def get_signed_url(path):
    bucket_location = s3_client.get_bucket_location(Bucket=S3_BUCKET)['LocationConstraint']
    url = "https://%s.s3.%s.amazonaws.com/%s" % (S3_BUCKET,bucket_location, path)
    return url


def construct_csv(image_batch):
    batch_no = image_batch["batch_number"]
    row = {}
    for i, image in enumerate(image_batch["images"]):
        for key in image:
            if key in IMAGE_PROPS:
                row[f"{key}_{i}"] = image[key]
            elif key == "path":
                row[f"{DATA_URL_COLUMN}_{i+1}"] = get_signed_url(image[key]) 
    f  = open(f"{BATCH_PATH}/batch_{batch_no}.csv", "w")
    writer = csv.DictWriter(f,list(row.keys()))
    writer.writeheader()
    writer.writerow(row)
    f.close()

def path_to_dict(file_name, folder_path):
    transaction_id, trial_id, trial_name, attack_id = file_name.split("-")
    return {
        "transaction_id": transaction_id,
        "trial_id": trial_id,
        "trial_name": trial_name,
        "attack_id": attack_id[:12],
        "attack_id_full": attack_id,
        "path": file_name
    }


def get_batches(folder_path):
    images = [path_to_dict(f, folder_path) for f in os.listdir(folder_path)]
    images.sort(key=lambda x: x["attack_id"])
    num_batches = math.ceil(len(images) / BATCH_SIZE)
    batches = {}
    i = 0
    for image in images:
        if batches.get(i):
            batches[i].append(image)
        else:
            batches[i] = [image]
        i = (i + 1) % num_batches
    return [{ "batch_number": k, "images": v } for k,v  in batches.items()]


if __name__ == "__main__":
    batches = get_batches(IMAGE_PATH)
    print(f"total {len(batches)}")
    i = 0
    for batch in batches:
        construct_csv(batch)
        print(f"{i+1} done")
        i += 1


