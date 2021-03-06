#  Copyright 2016-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0

import sys
from awsglue.transforms import Join
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
import time

glueContext = GlueContext(SparkContext.getOrCreate())

region_name = "{{ default_region }}"
crawler_name = "{{ glue_crawler_name }}"

# initiate the crawler
glue_client = boto3.client('glue', region_name=region_name)
response = glue_client.start_crawler(Name=crawler_name)

# wait for the crawler to finish
while True:
    state=glue_client.get_crawler(Name=crawler_name)
    status=state["Crawler"]
    st=status['State']
    if(st == 'RUNNING' or st == 'STOPPING'):
        time.sleep(1)
    else:
        break

# catalog: database and table names
db_name = "{{ glue_database_name }}"
tbl_persons = "persons_json"
tbl_membership = "memberships_json"
tbl_organization = "organizations_json"

# output s3 and temp directories
output_history_dir = "{{ glue_job_output_s3_location }}/legislator_history"
output_lg_single_dir = "{{ glue_job_output_s3_location }}/legislator_single"
output_lg_partitioned_dir = "{{ glue_job_output_s3_location }}/legislator_part"


# Create dynamic frames from the source tables
persons = glueContext.create_dynamic_frame.from_catalog(database=db_name, table_name=tbl_persons)
memberships = glueContext.create_dynamic_frame.from_catalog(database=db_name, table_name=tbl_membership)
orgs = glueContext.create_dynamic_frame.from_catalog(database=db_name, table_name=tbl_organization)

# Keep the fields we need and rename some.
orgs = orgs.drop_fields(['other_names', 'identifiers']).rename_field('id', 'org_id').rename_field('name', 'org_name')

# Join the frames to create history
l_history = Join.apply(orgs, Join.apply(persons, memberships, 'id', 'person_id'), 'org_id', 'organization_id').drop_fields(['person_id', 'org_id'])

# ---- Write out the history ----

# Write out the dynamic frame into parquet in "legislator_history" directory
print("Writing to /legislator_history ...")
glueContext.write_dynamic_frame.from_options(frame = l_history, connection_type = "s3", connection_options = {"path": output_history_dir}, format = "parquet")

# Write out a single file to directory "legislator_single"
s_history = l_history.toDF().repartition(1)
print("Writing to /legislator_single ...")
s_history.write.parquet(output_lg_single_dir)

# Convert to data frame, write to directory "legislator_part", partitioned by (separate) Senate and House.
print("Writing to /legislator_part, partitioned by Senate and House ...")
l_history.toDF().write.parquet(output_lg_partitioned_dir, partitionBy=['org_name'])

