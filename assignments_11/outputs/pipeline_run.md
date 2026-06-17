
Reflection
Write outputs/pipeline_run.md with a short reflection (4-6 sentences) covering:


1. Did the pipeline run cleanly on the first try? If not, what failed and how did you fix it?
The pipeline did not run cleanly on the first try because I had some Azure authentication issues. I fixed it by checking my Azure login and credentials.

2. What did the Prefect UI show? Were there any retries?

 In the Prefect UI, I could see the Extract, Transform, and Load tasks running in order and completing successfully. There were no retries during the final run.

3. 
What is one thing you would change or add if you were deploying this pipeline to run on a daily schedule?

If I deployed this pipeline every day, I would add email notifications to alert me if a task fails.