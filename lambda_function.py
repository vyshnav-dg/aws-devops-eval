import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        if event.get("source") == "aws.ec2" or event.get("source") == "aws.s3":
            ddb = boto3.resource("dynamodb")
            table = ddb.Table("EvalTable")
            item = {
                "event_time": event.get("time"),
                "event_source": event.get("source"),
                "event_name": event.get("detail-type"),
                "resource_name(s)": ", ".join(event.get("resources")),
                "aws_region": event.get("region"),
                "aws_username": event.get("account")
            }
            table.put_item(Item=item)
            logger.info("Item added to table")
            return {
                "statusCode": 200
            }

    except Exception as e:
        logger.error(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

