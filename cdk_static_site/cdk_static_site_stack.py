from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
)
from constructs import Construct


class CdkStaticSiteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_access_logs = s3.Bucket(
            self, "S3AccessLogs"
        )

        bucket = s3.Bucket(
            self, "CdkStaticSiteBucket",
            server_access_logs_bucket=s3_access_logs
        )

        s3_deploy.BucketDeployment(
            self, "CdkStaticSiteDeployment",
            sources=[s3_deploy.Source.asset("./site")],
            destination_bucket=bucket
        )

        cloudfront.Distribution(
            self, "CdkStaticSiteDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                # note: this creates an OAI implicitly. CDK doesn't support OAC.
                # https://github.com/aws/aws-cdk/issues/21771
                origin=cloudfront_origins.S3Origin(bucket=bucket),
                compress=True,
            ),
            default_root_object="index.html",

            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_page_path="/error/404.html")
            ],
            # implicitly creates a S3 bucket for logging and adds ACL for awslogsdelivery to it
            enable_logging=True
        )
