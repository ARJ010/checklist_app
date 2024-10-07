Here’s the corrected version of the README file in a single Markdown format without splitting any sections. You can copy and paste this into your `README.md` file in your GitHub repository:

```markdown
# CMS App

![CMS App Logo](link-to-your-logo) *(Optional)*

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [User Roles](#user-roles)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

## Introduction

The **CMS App** (Checklist Management System) is a robust Django application designed for Chartered Accountants to streamline checklist management. It provides various functionalities tailored to different user roles, enhancing productivity and efficiency.

## Features

- User authentication and role management
- Multi-user roles: Manager (Admin), User, and Checker
- Section management for organized checklists
- Intuitive user interface
- [Add more features as needed]

## Technologies Used

- **Django**: Web framework for building the application
- **Python**: Programming language used
- **SQLite/PostgreSQL**: Database management
- [Add other libraries or technologies as necessary]

## Installation

### Prerequisites

- Python 3.x
- Django
- pip

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cms_app.git
   cd cms_app
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the app at `http://127.0.0.1:8000/`

## Usage

- **Login**: Users can log in using their credentials.
- **Role-specific functionalities**:
  - **Manager**: Oversee app settings, manage users, and view reports.
  - **User**: Create and manage checklists.
  - **Checker**: Verify completed tasks.
- [Add additional usage instructions or examples]

## User Roles

- **Manager (Admin)**: Has full control over the application, including user management.
- **User**: Can create and manage checklists.
- **Checker**: Responsible for verifying tasks and providing feedback.

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: Abhinav Raj (Adithya P)
- **GitHub**: [yourusername](https://github.com/yourusername)
- **Email**: [your.email@example.com] *(Optional)*
```

### Customization:
- Replace `link-to-your-logo` with the actual URL of your logo if you have one.
- Update `yourusername` and `your.email@example.com` with your actual GitHub username and email.
- Modify any sections to add specific features or usage instructions as necessary.

Let me know if you need further assistance or any more adjustments!
