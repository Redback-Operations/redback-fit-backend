# Frontend Edits

These files include frontend changes that correspond to backend features.

## ProfilePage.tsx
Path in frontend repo: `src/routes/ProfilePage/ProfilePage.tsx`
- Updated to fetch and post user profile data from the backend API (`/api/profile`)
- Remove triple quoted comments in '/api/routes.py' 
- Requires backend to be running on `http://localhost:5000`
- Avatar changes work, but image persistence will depend on future storage logic

## Notes
Make sure to replace the file in the correct directory and test with the backend running.