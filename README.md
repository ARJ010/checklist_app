# Checklist Management System

This repository contains the source code for the **Checklist Management System**, a web application developed for **TH&Co**, a chartered accountant firm in Calicut, Kerala. The project is part of the Integrated M.Sc. in Computer Science with a specialization in Artificial Intelligence and Machine Learning by **Abhinav Raj**.

## Overview

The Checklist Management System (CMS) is designed to streamline the process of managing and verifying procedural checklists. The system automates task management, improves workflow efficiency, and enhances accuracy in task reviews.

### Key Features
- **Role-based Access Control**: Supports three roles—Admins, Users, and Checkers.
  - **Admins**: Manage users, checklists, and oversee the system.
  - **Users**: Submit forms and initiate procedures.
  - **Checkers**: Review submissions against checklists for compliance.
- **User-friendly Interface**: Built with HTML, CSS, and JavaScript for seamless interaction.
- **Backend**: Developed using Django with SQLite for efficient data management.
- **Security**: Role-based permissions and secure data handling.
- **Scalable Architecture**: Designed for future enhancements and growth.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Django Framework)
- **Database**: SQLite
- **Version Control**: Git, GitHub
- **IDE**: Visual Studio Code

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ARJ010/checklist_app.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd checklist_app
    ```
3. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5. **Run migrations** to set up the database:
    ```bash
    python manage.py migrate
    ```
6. **Start the development server**:
    ```bash
    python manage.py runserver
    ```
7. **Access the application** in your browser at `http://127.0.0.1:8000/`.

## Usage

- **Admin**: Create, update, and manage users and checklists.
- **User**: Submit forms and track the status of procedures.
- **Checker**: Review and verify submissions against checklists.

## Future Enhancements

- **Frontend Integration with React** for improved UI.
- **Advanced Analytics** for tracking performance metrics.
- **Mobile Compatibility** to access checklists on the go.

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch with your feature or bugfix.
3. Submit a pull request with detailed description of changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Developed by **Abhinav Raj**  
Integrated M.Sc. in Computer Science (AI & ML)
