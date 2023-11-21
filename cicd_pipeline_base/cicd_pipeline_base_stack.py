import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    ShellStep,
    ManualApprovalStep,
)

from cicd_pipeline_base.test_lambda_app_stage import MyPipelineAppStage


class CicdPipelineBaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "CicdPipelineBaseQueue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "CicdPipelineBaseTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth", 
                            input=CodePipelineSource.git_hub("OWNER/REPO", "main"),
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]))

        testing_stage = pipeline.add_stage(MyPipelineAppStage(self, "testing",
            env=cdk.Environment(account="111111111111", region="ap-northeast-1")))

        testing_stage.add_post(ManualApprovalStep('approval'))
