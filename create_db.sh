#!/bin/bash

echo "Which type of DB do you want to create? (mysql/postgres)"
read db_type

echo "Enter the database name:"
read db_name

echo "Enter the username:"
read username

echo "Enter the password:"
read -s password

echo "Enter the database host (IP address):"
read db_host

echo "Enter the database port:"
read db_port

if [ "$db_type" == "mysql" ]; then
    # Update the MySQL script with the provided database name
    sed "s/your_database_name/$db_name/g" create_mysql_db.sql > temp_mysql_db.sql

    # Create the MySQL database
    mysql -u "$username" -p"$password" -h "$db_host" -P "$db_port" < temp_mysql_db.sql

    # Cleanup
    rm temp_mysql_db.sql
elif [ "$db_type" == "postgres" ]; then
    # Update the PostgreSQL script with the provided database name
    sed "s/your_database_name/$db_name/g" create_postgresql_db.sql > temp_postgresql_db.sql

    # Create the PostgreSQL database
    PGPASSWORD="$password" psql -U "$username" -h "$db_host" -p "$db_port" -f temp_postgresql_db.sql

    # Cleanup
    rm temp_postgresql_db.sql
else
    echo "Invalid database type. Please enter either 'mysql' or 'postgres'."
    exit 1
fi

echo "Database created successfully."
