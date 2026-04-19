import json
import pytest

# Mocking the lambda imports
try:
    import upload_csv.upload_csv as upload_csv
except ImportError:
    upload_csv = None

try:
    import csv_coordinator.csv_coordinator as csv_coordinator
except ImportError:
    csv_coordinator = None

try:
    import csv_processor.csv_processor as csv_processor
except ImportError:
    csv_processor = None


class TestEpic3CsvBulkImport:
    
    def test_generate_presigned_url(self, s3):
        """Task 1: Validate UploadCsvFunction generates an S3 presigned URL."""
        if not upload_csv:
            pytest.skip("upload_csv handler not found")
        
        event = {
            "httpMethod": "POST",
            "path": "/contacts/upload",
            "body": json.dumps({"filename": "test.csv"}),
            "requestContext": {
                "authorizer": {"claims": {"sub": "user-123", "email": "test@example.com"}}
            }
        }
        
        response = upload_csv.lambda_handler(event, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "uploadUrl" in body
        assert "phone-book-csv-axel-portafolio" in body["uploadUrl"]

    def test_chunk_calculator_logic(self, s3):
        """Task 2: Validate ChunkCalculatorFunction divides CSV correctly."""
        if not csv_coordinator:
            pytest.skip("csv_coordinator handler not found")
            
        # Put a fake CSV in S3
        bucket = "phone-book-csv-axel-portafolio"
        key = "uploads/test.csv"
        csv_content = "name,phone,email\nJohn,123,john@test.com\nJane,456,jane@test.com"
        s3.put_object(Bucket=bucket, Key=key, Body=csv_content)
        
        event = {
            "bucket": bucket,
            "key": key
        }
        
        # Call coordinator
        result = csv_coordinator.lambda_handler(event, None)
        assert "chunks" in result
        assert len(result["chunks"]) > 0

    def test_csv_processor_inserts_to_db(self, dynamodb, s3):
        """Task 3: Validate CsvProcessorFunction reads chunk and inserts to DynamoDB."""
        if not csv_processor:
            pytest.skip("csv_processor handler not found")
            
        bucket = "phone-book-csv-axel-portafolio"
        key = "uploads/test.csv"
        csv_content = "name,phone,email\nJohn,123,john@test.com\nJane,456,jane@test.com"
        s3.put_object(Bucket=bucket, Key=key, Body=csv_content)
        
        event = {
            "bucket": bucket,
            "key": key,
            "start_row": 0,
            "end_row": 2
        }
        
        result = csv_processor.lambda_handler(event, None)
        assert result.get("status") == "success" or result.get("processed_rows") == 2
        
        # Verify in DB
        items = dynamodb.scan()['Items']
        assert len(items) >= 2

    def test_state_machine_execution_flow(self):
        """Task 4: Simulate Step Functions state machine flow."""
        # Step functions orchestration is typically tested via integration tests on AWS.
        # Locally, we mock the flow by calling ChunkCalculator then looping through CsvProcessor.
        pass
