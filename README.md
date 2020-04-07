

# Ansible Glue Example

This project shows how to use Ansible to deploy a complete glue application: database, crawler and job to AWS.
It is using the same files and exaples from AWS documentation:

https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-samples-legislators.html

It creates and deploy following items:
- IAM role for Glue
- S3 buckets
- Legislators sample json files
- Glue Database
- Glue Crawler
- Glue Python Job

Please note that the ansible script is not launching the crawler or job execution.
Before executing the job, you would need to run the crawler.
You can also choose to runthe crawler from the job script.



