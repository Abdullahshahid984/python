aws ecs describe-tasks --cluster your-cluster --tasks TASK_ARN --region eu-west-2 --query 'tasks[0].attachments[?name==`elasticNetworkInterface`].details[?name==`privateIPv4Address`].value'
