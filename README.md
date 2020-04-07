

# Ansible Glue Example

This project shows how to deploy a complete glue: database, crawler and job to AWS using Ansible.
It is using the same files from AWS documentation:

https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-samples-legislators.html

It creates and deploy following items:
- IAM role for Glue
- S3 buckets
- Legislators sample json files
- Glue Database
- Glue Crawler
- Glue Python Job


