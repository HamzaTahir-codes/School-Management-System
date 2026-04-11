# Manual Testing Guide: School Identity & Dashboards

Please follow these steps to verify that the implementation is working correctly.

## 1. Test New School Signup (Public Schema)
1. Go to your local signup page: `http://localhost:8000/signup/` (or whoever your primary domain is routed through).
2. Fill out the application form with a test school name, slug (e.g., `test-school`), your email, and a password.
3. **Verify**: You should see the newly added fields: **School Tagline** and **About School**. Fill them out with some test data.
4. Submit the form. It should redirect you to the new school's login page (e.g., `http://test-school.localhost:8000/login/`).

## 2. Test the New Public Landing Page
1. While **logged out**, visit your newly created school's root domain: `http://test-school.localhost:8000/`
2. **Verify**: You should see the new, beautifully designed "SchoolOS" Landing page.
3. Check that the **School Name**, **Tagline**, and **About** text from your signup successfully loaded into the template.
4. Verify the animated blobs in the background are rendering smoothly.
5. Click **"Sign In"** in the top right corner. It should take you to the standard login page.

## 3. Test the Module Root URLs
1. Log in with your new admin account.
2. In your browser's address bar, directly visit the root paths of the following modules:
    - `http://test-school.localhost:8000/people/`
    - `http://test-school.localhost:8000/academics/`
    - `http://test-school.localhost:8000/attendance/`
    - `http://test-school.localhost:8000/grading/`
    - `http://test-school.localhost:8000/fees/`
    - `http://test-school.localhost:8000/certificates/`
    - `http://test-school.localhost:8000/ai/`
    - `http://test-school.localhost:8000/notifications/`
3. **Verify**: None of these urls should return a `Page Not Found (404)`.
4. **Verify**: As an admin, they should all display beautifully styled "Module Dashboards" (except notifications which should just show your inbox).
5. **Verify Security**: Log out, then log in as a regular Teacher or Student. Try to visit those same links (e.g. `/ai/`). You should be instantly redirected back to your dashboard with a toast saying "You are not authorized to visit this page".
6. Open an incognito window without logging in and try navigating to those module paths directly.
7. **Verify**: They should all seamlessly redirect you to the login page (or the School Page for `/ai/`).

## 4. Test School Identity Settings
1. Logged in as your Admin, open the left sidebar.
2. Look at the bottom under "Profile Settings". You should see a new link: **"School Identity"**.
3. Click it and access the identity settings page.
4. **Verify**: Ensure the form displays prefilled with your Tagline and About Text. 
5. Fill out the **Mission** and **Vision** fields.
6. Upload a random image as the **Logo**.
7. Click **Save Identity Settings**.
8. Log out (or open an incognito window) and visit `http://test-school.localhost:8000/` again.
9. **Verify**: Confirm that the new Logo appears in the top left, and the Mission/Vision sections successfully render near the bottom.
