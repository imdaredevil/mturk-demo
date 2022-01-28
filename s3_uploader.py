import boto3
from botocore.exceptions import ClientError
import json
import os

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


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    files = [f"{IMAGE_PATH}/{f}" for f in sorted(os.listdir(IMAGE_PATH))]
    i = 0
    for file_name in files:
        upload_file(file_name, S3_BUCKET)
        i += 1
        if i % 10 == 0:
            print(f"{i} done")
