# chatgpt4bot

To run the script, make sure it's executable:
```
bash
Copy code
chmod +x create_db.sh
```
Then, execute the script:

```
bash
Copy code
./create_db.sh
```
Follow the prompts and enter the requested information. The script will create the appropriate database based on your input.

Replace the placeholders with your own values:
```
your_openai_api_key: Your OpenAI API key.
your_openai_api_model: The OpenAI API model you want to use (e.g., "text-davinci-002").
your_twilio_phone_number: Your Twilio phone number.
your_database_type: The type of database you're using ("mysql", "postgres", or "sqlite").
your_database_user: The username for your MySQL or PostgreSQL database (not needed for sqlite DB).
your_database_password: The password for your MySQL or PostgreSQL database (not needed for sqlite DB).
your_database_host: The host (IP address or domain) of your MySQL or PostgreSQL database (not needed for sqlite DB).
your_database_name: The name of your MySQL or PostgreSQL database (not needed for sqlite DB).
your_database_port: The port number for your MySQL or PostgreSQL database (not needed for sqlite DB).
```
Save this template as .env in the same directory as your main.py and dbhandler.py files. The application will automatically load the environment variables from the .env file.

You can use dbmanager.py in order to clear and display the content of the database

usage: dbmanager.py [-h] [--clear]
                           [--display]
```
DB Manager

options:
  -h, --help  show this help message and exit
  --clear     Clear the DB
  --display   Display the DB contents
  ```
