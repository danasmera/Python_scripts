#!/usr/bin/env python

''' Recursively list all files in S3 under your account '''
try:
    import boto.ec2
except Exception as e:
    raise Exception(e)
s3conn = boto.connect_s3()
print("All buckets - \n")
for mybkt in s3conn:
    print mybkt.name
print("\n\n")
# All keys in a bucket
print "Recurse across all buckets - \n"
for mybkt in s3conn:
    print("Bucket name : {0}".format(mybkt.name))
    for item in mybkt.get_all_keys():
        print(item.name)
