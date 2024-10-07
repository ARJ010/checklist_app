# Checklist Management System

A comprehensive web-based application designed to automate and streamline checklist management processes, particularly for chartered accountant firms. Developed using **Django** and **SQLite**, the system provides role-based access control for Admins, Users, and Checkers, ensuring efficient workflow, accuracy in form reviews, and comprehensive oversight.

## Project Overview

This project was developed as part of the degree requirements for **Integrated M.Sc. in Computer Science with a specialization in Artificial Intelligence and Machine Learning** at **Nehru Arts and Science College, Kanhangad** under **Kannur University**.

The Checklist Management System (CMS) was created to replace manual checklist processes at **TH&Co**, a chartered accountant firm in Kerala, with a web-based solution that automates checklist generation, submission, and review.

## Features

- **Role-Based Access Control**:
  - **Admin**: Manage users, roles, checklists, and system operations.
  - **User**: Initiate procedures, submit forms, and interact with checklists.
  - **Checker**: Review and verify form submissions against the checklist criteria.
  
- **User Authentication**: Secure login system with password protection.
  
- **Checklist and Procedure Management**:
  - Create and manage custom checklists.
  - Track the status of procedure submissions.
  - Receive feedback and resubmit forms when necessary.
  
- **Admin Dashboard**: View performance metrics, manage users and checklists, and access historical data.
  
- **Automated Notifications**: Real-time alerts for task status updates, ensuring timely action by users and checkers.
  
- **Data Security**: Role-based access and data protection mechanisms to safeguard sensitive client information.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Version Control**: Git

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ARJ010/checklist_app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd checklist_app
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`.

## Usage

- **Admin**: 
  - Log in using admin credentials.
  - Navigate to the admin dashboard to manage users, checklists, and review performance metrics.

- **User**: 
  - Log in to submit forms, select checklists, and track the progress of submissions.

- **Checker**: 
  - Review submitted forms against checklist criteria and provide feedback or approve the submissions.

## Future Enhancements

- **Frontend Improvements**: Integrating React for a more dynamic and responsive user interface.
- **Advanced Analytics**: Incorporating data-driven insights for better performance tracking and decision-making.
- **Mobile Compatibility**: Ensuring seamless access to the system from mobile devices.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Author

**Abhinav Raj**  
[GitHub](https://github.com/ARJ010)

---
