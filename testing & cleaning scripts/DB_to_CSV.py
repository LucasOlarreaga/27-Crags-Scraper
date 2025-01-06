import sqlite3
import csv

def db_to_csv(db_file, csv_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query all data from the database
    cursor.execute("SELECT * FROM climbs")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Write data to CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)  # Write column names
        csvwriter.writerows(rows)  # Write data rows

    # Close the database connection
    conn.close()

# Example usage
db_file = 'files/merged_climbs.db'
csv_file = 'Merged_Climbs.csv'
db_to_csv(db_file, csv_file)