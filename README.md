   aws ecs describe-tasks --cluster local-sites-forms-runner-dev-cluster --tasks YOUR_TASK_ARN --region eu-west-2 --query 'tasks[0].attachments[0].details' --output table
