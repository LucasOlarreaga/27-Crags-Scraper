# Main function
import sqlite3

# Path to SQLite database
db_path = "files/merged_climbs.db"

grades_hash = {
    1300: 17, 1350: 18, 1400: 19,
    1450: 20, 1500: 21, 1550: 22, 1600: 23
}

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Add a new column for numeric grades
    #cursor.execute("ALTER TABLE climbs ADD COLUMN grade_numeric INTEGER")

    # Update the new column with numeric values from the grade column
    #cursor.execute("UPDATE climbs SET grade_numeric = CAST(grade AS INTEGER)")

    # Verify the update by selecting unique values
    cursor.execute("SELECT DISTINCT grade_numeric FROM climbs")
    test = cursor.fetchall()
    for row in test:
        grade_numeric = row[0]
        if grade_numeric in grades_hash:
            cursor.execute(
                "UPDATE climbs SET grade_numeric = ? WHERE grade_numeric = ?",
                (grades_hash[grade_numeric], grade_numeric)
            )
    
     # Verify the update by selecting unique values
    cursor.execute("SELECT DISTINCT grade_numeric FROM climbs WHERE grade_numeric > 17")
    test = cursor.fetchall()
    for row in test:
        print(row)

    # Remove the grades column from the climbs table
    cursor.execute("ALTER TABLE climbs DROP COLUMN grade")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

  

if __name__ == "__main__":
    main()