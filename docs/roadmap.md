Project Roadmap: Scalable TinyURL Service on AWS
Weekly Commitment: 15 hours
Support: Guidance from an experienced mentor.
Total Estimated Timeline: 5 Weeks
Project Goal
To build a scalable URL shortening service, similar to TinyURL, hosted on AWS. The service will support standard and custom short links, employ a caching layer for performance, and use tiered storage for cost efficiency. This project emphasizes a professional workflow using Infrastructure as Code (IaC) and a CI/CD pipeline.
Core Technologies
Programming Language: Python
Infrastructure as Code (IaC): AWS SAM (Serverless Application Model)
CI/CD: GitHub Actions
Primary Database: Amazon DynamoDB
Caching: Amazon ElastiCache for Redis
Long-Term Storage: Amazon S3
Compute: AWS Lambda & Amazon API Gateway
API Testing: Postman (or similar API client)
High-Level Plan: Phased Rollout
This table provides a high-level overview of the project, breaking it down into distinct product releases. Use this to track your overall progress.
Milestone
Phase
Core Objective
Status
1. CI/CD Pipeline
MVP
"Make it build." Establish a reliable, automated foundation for all future development and deployment.
DONE


2. Foundational Service
MVP
"Make it work." Implement the core logic for creating and storing short links.
ALMOST DONE
3. Redirection
MVP
"Make it useful." Enable the redirection functionality that makes the short links work.


4. Caching
MMP
"Make it fast." Integrate a caching layer to ensure the service is performant and scalable.


5. Storage Tiering
MMP
"Make it efficient." Implement a long-term storage strategy to ensure the service is cost-effective to operate.


6. Custom URLs
MLP
"Make it personal." Enhance the API to support user-defined, custom short links.



Detailed Execution Plan
This section provides the specific tasks and deliverables for each milestone.
Milestone 1: CI/CD Pipeline with AWS SAM & GitHub Actions - DONE
Phase: MVP
Time Estimate: 1 Week
Goal: Automatically deploy a simple "Hello World" serverless application to AWS from your GitHub repository every time you push to the main branch.
Mentor Guidance: This is the perfect place to lean on your mentor. Ask them about best practices for IAM permissions and managing secrets for CI/CD. Getting the initial pipeline right is crucial.
Tasks:
Setup AWS & GitHub: Create a GitHub repository and an IAM User in AWS for GitHub Actions. Store the keys as repository secrets.
Create a "Hello World" App: Use the AWS SAM CLI (sam init) to generate a starter application.
Build the GitHub Action Workflow: Create a .github/workflows/deploy.yml file to define the pipeline steps (checkout, configure AWS, build, deploy).
Deliverable: A fully automated pipeline. Pushing a change to main triggers a deployment, and you get a public API Gateway URL that returns a "Hello World" message.
Milestone 2: Foundational Shortening Service - ALMOST DONE
Implement Base62 encoding for short_id, Add unit tests, Rename any remaining HelloWorld references, Add a custom domain (e.g., tariksurl.com) 
Phase: MVP
Time Estimate: 1 Week
Goal: Replace the "Hello World" function with the core URL shortening logic.
Mentor Guidance: Discuss your DynamoDB schema design with your mentor. Ask about choosing the right primary key for efficient lookups and avoiding hot partitions.
Tasks:
Modify template.yaml to define a DynamoDB table.
Update the Lambda function code to handle a POST request, generate a unique short ID, and save the mapping to DynamoDB.
Update the API Gateway in template.yaml to handle POST /shorten.
 Deliverable: Your CI/CD pipeline deploys a version that can shorten a URL and store it in DynamoDB. You can test this endpoint using Postman.
Milestone 3: Redirection
Phase: MVP
Time Estimate: 1 Week
Goal: Enable redirection from a short URL to the original URL.
Mentor Guidance: Ask your mentor about the best way to return errors from API Gateway (e.g., 404 Not Found).
Tasks:
Create a second Lambda function for redirection logic.
Update template.yaml to add a GET /{short_id} endpoint that triggers the redirection Lambda.
 Deliverable: A deployed service that can successfully redirect a shortened URL to its original destination when visited in a browser.
Milestone 4: Caching with Redis
Phase: MMP
Time Estimate: 1 Week
Goal: Implement a caching layer to improve redirection performance.
Mentor Guidance: This is a great time to discuss caching strategies (e.g., cache-aside pattern, TTL selection) and the trade-offs between performance, cost, and data consistency.
Tasks:
Add an Amazon ElastiCache for Redis cluster resource to your template.yaml.
Modify your redirection Lambda to implement the cache-aside pattern: check Redis first, and on a miss, query DynamoDB and populate the cache.
 Deliverable: A faster redirection service that uses caching to minimize database lookups.
Milestone 5: Storage Tiering & Optimization
Phase: MMP
Time Estimate: 1 Week
Goal: Move old, infrequently accessed URLs to cheaper S3 storage and retrieve them when needed.
Mentor Guidance: Discuss the design of the archival and retrieval process. Ask about error handling and the potential for a "thundering herd" problem if a popular archived link is suddenly accessed.
Tasks:
Create a scheduled Lambda function (triggered by Amazon EventBridge) that archives old DynamoDB entries to S3.
Update your redirection Lambda to query S3 if an ID is not found in the cache or DynamoDB.
Implement logic to "re-hydrate" an archived link back into DynamoDB and Redis upon access.
 Deliverable: A fully-featured, cost-optimized system that intelligently manages data across different storage layers.
Milestone 6: Custom URLs
Phase: MLP
Time Estimate: 1 Week
Goal: Allow users to create custom-named short links via the API.
Mentor Guidance: Ask your mentor about handling potential race conditions when checking for custom alias availability. Discuss how to return clear user-facing errors (e.g., 409 Conflict if an alias is taken).
Tasks:
Modify the /shorten endpoint to optionally accept a custom_alias in the request body.
Implement logic to check if the alias is already taken in DynamoDB before creating the new item.
 Deliverable: An updated API that supports creating both random and custom-named short links, testable via Postman.
Future Extensions (MLP+)
Web Front-End: Create a simple HTML/CSS/JS user interface to make the service accessible without an API client.
URL Analytics: Create a new endpoint (e.g., GET /{short_id}/stats) that returns click-count data. This would involve updating the redirection Lambda to increment a counter in DynamoDB on each hit.
User Accounts: Introduce user authentication (e.g., with Amazon Cognito) to allow users to manage their own links.
