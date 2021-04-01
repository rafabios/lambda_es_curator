# lambda_es_curator
Lambda function for AWS ES Curator



```bash
git clone https://github.com/rafabios/lambda_es_curator.git

cd lambda_es_curator/
pip install -r requirements.txt -t .
zip -r9 ~/lambda.zip .
```  



#### Then upload this `lambda.zip` to AWS Lambda

You must set the following variables:

| Variable | Value |
| ------ | ------ |
| ES_HOST | search-xxxxxxxxx.xx-xxx-x.es.amazonaws.com |
| ES_PASSWORD | this_is_my_password |
| ES_LOGIN | admin |
| ES_SSL | True |
| ES_SSL_VERIFY | True |
| ES_EXCEPT_INDICES | kibana,opendistro  #separated by comma |
| ES_UNIT | days |
| ES_UNIT_COUNT | 7 |

This variables connects to AWS ES domain and delete all indices except kibana and opendistro in a period later than 7 days.

# AWS Settings

Lambda Settings:

- [Language/Version] - Python 3.6
- [Memory] - 128Mb
- [Function_Name] - lambda_function/lambda_handler
