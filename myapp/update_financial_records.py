import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host=DATABASES['default']['HOST'],
    user=DATABASES['default']['USER'],
    password=DATABASES['default']['PASSWORD'],
    database=DATABASES['default']['NAME']
)
cursor = connection.cursor()

try:
    # Select all distinct user IDs from the users table
    cursor.execute("SELECT DISTINCT ID FROM users")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        user_id = user_id[0]  # Extract the user ID from the tuple
        # Insert random records into the financial_records table for the current user
        cursor.execute("""
            INSERT INTO financial_records (user_id, record_date, title, amount)
            SELECT 
                %s, 
                CURDATE(), 
                CONCAT('Expense_', FLOOR(RAND() * 1000)), 
                ROUND(RAND() * 1000, 2)
            FROM 
                information_schema.tables
            LIMIT 
                10
        """, (user_id,))

        # Update the money_spent value for the current user in the users table
        cursor.execute("""
            UPDATE users AS u
            SET u.money_spent = (
                SELECT SUM(fr.amount)
                FROM financial_records AS fr
                WHERE fr.user_id = %s
            )
            WHERE u.ID = %s
        """, (user_id, user_id))

    # Commit changes to the database
    connection.commit()
    print("Records updated successfully for all users.")

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
