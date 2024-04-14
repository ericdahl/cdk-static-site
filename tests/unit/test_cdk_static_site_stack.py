import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_static_site.cdk_static_site_stack import CdkStaticSiteStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_static_site/cdk_static_site_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkStaticSiteStack(app, "cdk-static-site")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
