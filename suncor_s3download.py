import boto3, botocore, os, pprint

# GLOBAL VARIABLES
IMAGE_PATH = '/var/www/utils.solspec.solutions/html/suncor/images/'
BUCKET_NAME = 'suncor-images'

# download recursively, maintaining file structure
s3 = boto3.client('s3')
s3objs = s3.list_objects(Bucket=BUCKET_NAME)

# print all file keys
#for obj in s3objs.get('Contents'):
#       print(obj['Key'])

# create directory structure
for obj in s3objs.get('Contents'):
        # only grab JPGs
        if 'JPG' in obj['Key']:
                filename = obj['Key'].split('/')[-1]
                directory = '/'.join(obj['Key'].split('/')[:-1])
                if not os.path.exists(IMAGE_PATH + directory):
                        os.makedirs(IMAGE_PATH + directory)
                if not os.path.exists(IMAGE_PATH + obj['Key']):
                        s3.download_file(BUCKET_NAME, obj['Key'], IMAGE_PATH + obj['Key'])
                        print('Downloaded: ' + filename)
                else:
                        print('Skipped: ' + filename)
