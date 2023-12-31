# MySQL Backup Script

## Overview

This script performs automated backups of a MySQL database using the `mysqldump` command. It allows you to schedule daily backups and provides a notification upon successful completion.

## Features

- **Automated Backups:** Schedule daily backups of your MySQL database.
- **Notification:** Receive notifications upon successful completion of the backup.
- **Backup Verification:** Verify the integrity of the backup file.

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages (install using `pip install -r requirements.txt`):
  - `pymysql`
  - `schedule`

## Configuration

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/your_repository.git
    ```

2. Install required packages:
    ```bash
   pip install -r requirements.txt
    ```

3. Environmental variables
    Create a .env file with values for the following:
    - DB_HOST=
    - DB_PORT=
    - DB_USER=
    - DB_PASS=
   
## Usage
Run the script from the command line:
    ```bash
    python main.py --database your_database --dir /path/to/backup/directory
    ```

## Troubleshooting
If you encounter any issues, refer to the logs for error messages. Common issues include:

- Incorrect MySQL credentials.
- Inaccessible backup directory.

## Contributing
If you'd like to contribute to this project, please follow the standard GitHub fork and pull request process.

## License
This project is licensed under the MIT License - see the LICENSE file for details.