import aws_cdk as cdk
import aws_cdk as core
import aws_cdk.assertions as assertions
from cicd_pipeline_base.cicd_pipeline_base_stack import CicdPipelineBaseStack


app = core.App()
pipeline_stack = CicdPipelineBaseStack(
    app,
    "cicd-pipeline-base",
    env=cdk.Environment(account="111111111111", region="ap-northeast-1")
)


def test_sqs_queue_created():
    template = assertions.Template.from_stack(pipeline_stack)
    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    template = assertions.Template.from_stack(pipeline_stack)

    template.resource_count_is("AWS::SNS::Topic", 1)


def pipeline_created():
    template = assertions.Template.from_stack(pipeline_stack)

    template.resource_count_is("AWS::CodePipeline::Pipeline", 1)
