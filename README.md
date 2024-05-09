# Python Web Server

## Prerequisites

- Python 3.8 or higher
- pip for installing dependencies

## Setup Environment

To set up the necessary environment, copy the example environment file to `.env`:

```bash
cp .env.example .env
```

## Install Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Server

To run the server, execute the following command:

```bash
python3 server.py
```

## Features

### User Authentication

- **Login**: Allows a user to log in to the system.
- **Register**: Allows a new user to register.
- **Logout**: Logs out the current user.

### Task Management

- **Get Tasks**: Retrieve a list of all tasks.
- **Add Task**: Add a new task to the list.
- **Delete Task**: Delete an existing task from the list.
