#CHECK_HTTP_LAMBDA

##Install Node dependencies

```
npm install q
npm install request
```

##Web List
Include your **URL Webs, methods and params** in **list.json** and upload it to **S3** in AWS

##SNS TOPIC
Create a **SNS topic** in AWS and verify your account.

##Create role for lambda
Create a IAM role in AWS, apply **policy.json** and set your **S3 Bucket** and **SNS ARN**

##Upload Lambda
Crate a package zip with code and dependencies and upload it to a Lambda function.
