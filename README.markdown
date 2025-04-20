# VotingApp

A simple Django-based voting application with admin and user functionalities.

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd VotingApp
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Admin User**: Run the following command to create the admin user with username "admin" and password "1234":

   ```bash
   python manage.py shell
   >>> from voting.models import AdminUser
   >>> AdminUser.objects.create(username="admin", password="1234")
   >>> exit()
   ```

6. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

7. **Access the App**:

   - Open your browser and go to `http://127.0.0.1:8000/`.
   - Use the admin login at the top right (username: `admin`, password: `1234`).

## Features

- **Homepage**: Cast vote button and admin login icon.
- **Admin Login**: Custom login for admins.
- **Admin Dashboard**: View total votes, edit candidates, reset votes.
- **Edit Candidates**: Add/remove candidates and start voting (minimum 2 candidates).
- **Voting**: Users enter their name, select a candidate, and submit their vote.
- **File Storage**: Uses `Voters.txt`, `candidates.txt`, and `vcount.txt` for data.
- **Styling**: Modern, simple CSS design.

## Notes

- Change the admin username/password in the database for production.
- The `SECRET_KEY` in `settings.py` should be changed for production.
- File-based storage is used for simplicity; consider a database for scalability.