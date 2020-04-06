#!/bin/bash

aaca -D --aws-region us-east-2

ansible-galaxy role init glue-cleate

aws glue start-crawler --name "wdl-aabg-glue-crawler"

aws glue get-crawler --name "wdl-aabg-glue-crawler"

aws s3 sync s3://awsglue-datasets/examples/us-legislators/all /Users/marian.dumitrascu/Dropbox/Work/current/VISTRA/wdl-glue/z-temp/legislators --region us-east-1

aws s3 cp s3://WholeBucket LocalFolder --recursive

aws s3 cp /Users/marian.dumitrascu/Dropbox/Work/current/VISTRA/wdl-glue/z-temp/legislators s3://eap-aabg-s3-landingzone/legislators --recursive
