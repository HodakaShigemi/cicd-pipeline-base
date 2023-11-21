#!/usr/bin/env python3

import aws_cdk as cdk

from cicd_pipeline_base.cicd_pipeline_base_stack import CicdPipelineBaseStack


app = cdk.App()
CicdPipelineBaseStack(
    app,
     "CicdPipelineBaseStack",
     env=cdk.Environment(account="111111111111", region="ap-northeast-1")
)

app.synth()
