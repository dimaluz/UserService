# USER Service – Microservice for Email Marketing App

[![Build Status](https://github.com/dimaluz/UserService/actions/workflows/pytest.yaml/badge.svg)](https://github.com/dimaluz/UserService/actions/workflows/pytest.yaml)


USER Service is a microservice designed for managing users within an email marketing application. This project is built with Django and includes Docker for seamless setup and deployment.

---

## Quick Start

> **Note:** This project requires **Python 3.11** and **Docker** to run.  
> **Note:** The root directory of the Django project is located within the `user_service` folder.

### Setting Up for Development

Follow these steps to set up the project for local development:

1. **Install Docker**  
   Ensure Docker is installed on your local machine. Visit [Docker's website](https://www.docker.com/get-started) for instructions.

2. **Install pre-commit**  
   Ensure `pre-commit` is installed on your local machine:
   ```bash
    pip install pre-commit
   ```
3. **Clone the Project**  
   Clone this repository to your local machine from `dev` branch:
   ```bash
    git clone https://github.com/dimaluz/UserService.git
   ```
4. **Set Up Environment Variables**  
   Create the `.env` file from the provided example and edit it to add your configuration:
   ```bash
    cp .env.template .env
    # Open .env and modify values as needed
   ```
5. **Build and Run Docker Containers**  
   Build the Docker containers:
   ```bash
    docker-compose --env-file ./user_service/.env up --build
   ```
6. **Make Migrations**  
   Make migrations by using those commands:
   ```bash
    docker-compose --env-file ./user_service/.env run --rm user_service bash -c "python manage.py makemigrations"
    docker-compose --env-file ./user_service/.env run --rm user_service bash -c "python manage.py migrate"
   ```
7. **Create Super User (First-Time Setup Only)**  
   Create a superuser to have an access to your admin pannel:
   ```bash
    docker-compose --env-file ./user_service/.env run --rm user_service bash -c "python manage.py createsuperuser"
   ```
8. **Run pre-commit**  
   Run `pre-commit` in the current repository:
   ```bash
    pre-commit install
    pre-commit run --all-files
   ```

---

### Project Structure

- **`user_service/`**: This is Root folder, which contains the Django project files and config folder with all settings.
- **`docker-compose.yml`**: Defines services and configuration for Docker containers.
- **`.env`**: Stores environment variables for the project (copy from `.env.example`).

### Contributing

To contribute to this project, please fork the repository, create a feature branch, and submit a pull request. For any issues, please open a ticket.
