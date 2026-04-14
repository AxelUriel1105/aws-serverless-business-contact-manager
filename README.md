# AWS Serverless Business Contact Manager

An optimized, scalable, and cost-efficient solution for managing enterprise-level contact databases. This project demonstrates a robust cloud architecture designed to handle everything from daily CRUD operations to massive data ingestion tasks.

## 🚀 Business Value
Traditional contact managers often struggle with large-scale data imports or incur high idle costs. This solution solves both:

* **Cost Efficiency:** Built on a "Pay-as-you-go" model; costs are $0 when not in use.
* **Infinite Scalability:** Seamlessly scales from a few dozen contacts to millions.
* **High Performance:** Processes 1,000,000+ records in a high-concurrency parallel pipeline.
* **Enterprise Security:** Fully integrated with AWS Cognito for identity management and CloudFront OAC for secure content delivery.

## 🛠 Tech Stack
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla).
* **Compute:** AWS Lambda (Python 3.9).
* **Orchestration:** AWS Step Functions (Express Workflows).
* **Database:** Amazon DynamoDB (On-Demand).
* **Storage:** Amazon S3.
* **Security:** AWS Cognito & IAM.
* **API/Networking:** Amazon API Gateway & Amazon CloudFront.
* **Infrastructure as Code:** AWS SAM (Serverless Application Model).

## 🏗 Architecture Overview
* **Identity:** Users authenticate via AWS Cognito to obtain a JWT token.
* **Web Delivery:** The frontend is hosted in a private S3 bucket, served globally via CloudFront with Origin Access Control (OAC).
* **API Layer:** API Gateway validates JWT tokens before triggering backend logic.
* **Data Ingestion:** Large CSV files uploaded to S3 trigger an EventBridge rule, starting a Step Function that coordinates parallel Lambda workers to process data chunks into DynamoDB.

## 📥 Getting Started

### Prerequisites
* AWS CLI configured with appropriate permissions.
* AWS SAM CLI installed.
* Python 3.9.

### 1. Infrastructure Deployment
Clone the repository and run the deployment pipeline:
```bash
sam build
sam deploy
```
Note: During deployment, SAM will provision all necessary resources including DynamoDB tables, Cognito User Pools, and S3 buckets.

2. Frontend Configuration
Once the deployment is complete, the terminal will display several Outputs. Use these values to connect your frontend:
  1. Open frontend/index.html.
  2. Locate the configuration constants at the beginning of the <script> tag.
  3. Update the values with your unique deployment outputs:
    - API_URL: Your generated API Gateway endpoint.
    - CLIENT_ID: Your Cognito App Client ID.
    - COGNITO_URL: The Identity Provider URL for your region (e.g., https://cognito-idp.us-east-1.amazonaws.com).

3. Static Content Upload
Upload the configured frontend to your private S3 bucket:
```bash
aws s3 sync frontend/ s3://phone-book-front-axel-portafolio --delete
```
4. Cache Invalidation
To ensure your changes are visible immediately through the CDN:
```bash
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```
## 📊 Performance Testing
To test the 1M records ingestion:
1. Run the generation script located in functions/one_mln_rows/one_mln_rows.py.
2. Upload the resulting contacts_1mln.csv to the S3 bucket named phone-book-csv-axel-portafolio.
3. Monitor the execution in the Step Functions console to see the parallel processing in action.
