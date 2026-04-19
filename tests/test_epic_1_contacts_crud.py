import json
from unittest.mock import patch
# Note: we use place holder imports, assuming lambda files are structured this way
# If the exact file name is different, imports need to be adjusted.
import insert_contact.insert_contact as insert_contact
import get_contacts.get_contacts as get_contacts
import get_contact.get_contact as get_contact
import update_contact.update_contact as update_contact
import delete_contact.delete_contact as delete_contact

def create_api_gateway_event(method, path, body=None, pathParameters=None):
    return {
        "httpMethod": method,
        "path": path,
        "body": json.dumps(body) if body else None,
        "pathParameters": pathParameters or {},
        "requestContext": {
            "authorizer": {
                "claims": {
                    "sub": "user-123",
                    "email": "test@example.com"
                }
            }
        }
    }

class TestEpic1ContactsCRUD:
    
    def test_insert_contact_success(self, dynamodb):
        """Task 1: Validate InsertContactFunction saves to DynamoDB."""
        event = create_api_gateway_event("POST", "/contacts", body={
            "userId": "contact-001",
            "name": "John Doe",
            "phone": "1234567890",
            "email": "john@example.com"
        })
        
        # Call handler (assuming lambda_handler exists)
        response = insert_contact.lambda_handler(event, None)
        
        assert response["statusCode"] == 200 or response["statusCode"] == 201
        
        # Verify in DB
        table = dynamodb
        db_response = table.get_item(Key={'userId': 'contact-001'})
        assert 'Item' in db_response
        assert db_response['Item']['name'] == "John Doe"

    def test_get_contacts_success(self, dynamodb):
        """Task 2: Validate GetContactsFunction returns correct data."""
        dynamodb.put_item(Item={'userId': 'contact-002', 'name': 'Jane Doe'})
        
        event = create_api_gateway_event("GET", "/contacts")
        response = get_contacts.lambda_handler(event, None)
        
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert isinstance(body, list) or "contacts" in body
        
    def test_update_contact_success(self, dynamodb):
        """Task 3: Validate UpdateContactFunction modifies existing data."""
        dynamodb.put_item(Item={'userId': 'contact-003', 'name': 'Old Name'})
        
        event = create_api_gateway_event("PUT", "/contacts/contact-003", body={
            "name": "New Name"
        }, pathParameters={"userId": "contact-003"})
        
        response = update_contact.lambda_handler(event, None)
        assert response["statusCode"] == 200
        
        # Verify in DB
        db_response = dynamodb.get_item(Key={'userId': 'contact-003'})
        assert db_response['Item']['name'] == "New Name"

    def test_delete_contact_success(self, dynamodb):
        """Task 4: Validate DeleteContactFunction removes data."""
        dynamodb.put_item(Item={'userId': 'contact-004', 'name': 'To Delete'})
        
        event = create_api_gateway_event("DELETE", "/contacts/contact-004", pathParameters={"userId": "contact-004"})
        
        response = delete_contact.lambda_handler(event, None)
        assert response["statusCode"] == 200 or response["statusCode"] == 204
        
        # Verify in DB
        db_response = dynamodb.get_item(Key={'userId': 'contact-004'})
        assert 'Item' not in db_response
