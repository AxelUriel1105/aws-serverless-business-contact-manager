import pytest
from playwright.sync_api import Page, expect

# To run these tests you need an actual frontend URL or localhost server.
# Set this to your local dev server or cloudfront distribution url.
FRONTEND_URL = "http://localhost:8080"  # Example local url

@pytest.mark.skip(reason="Needs a running frontend server to execute E2E tests.")
class TestEpic4FrontendE2E:
    
    def test_initial_render_success(self, page: Page):
        """Task 1: Validate frontend loads correctly."""
        page.goto(FRONTEND_URL)
        # Assuming there is a title or header with text 'Phone Book'
        expect(page).to_have_title("Phone Book App")
        expect(page.locator("h1")).to_contain_text("Phone Book")

    def test_login_flow(self, page: Page):
        """Task 2: Simulate login flow with Cognito."""
        page.goto(FRONTEND_URL)
        
        # Fill in credentials
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "Password123!")
        page.click("button[type='submit']")
        
        # Verify redirect or UI change (e.g. Dashboard appears)
        expect(page.locator(".dashboard-container")).to_be_visible()

    def test_create_contact_ui(self, page: Page):
        """Task 3: Create a contact via the UI."""
        # Setup: Be logged in (in practice, use a fixture to keep session)
        page.goto(f"{FRONTEND_URL}/dashboard")
        
        page.click("text=Add Contact")
        page.fill("input[name='name']", "E2E Test User")
        page.fill("input[name='phone']", "9998887777")
        page.click("button:has-text('Save')")
        
        # Verify contact appears in the list
        expect(page.locator("text=E2E Test User")).to_be_visible()

    def test_upload_csv_ui(self, page: Page):
        """Task 4: Upload CSV file via the UI."""
        page.goto(f"{FRONTEND_URL}/dashboard")
        
        # Set files to file input
        # page.set_input_files("input[type='file']", "tests/fixtures/sample.csv")
        # page.click("button:has-text('Upload CSV')")
        
        # Verify upload success message
        # expect(page.locator(".alert-success")).to_contain_text("Upload started")
        pass
