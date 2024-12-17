import sqlite3

# Path to SQLite database
db_path = "files/crags.db"

def font_grading(path, cursor, conn):
    # Mapping from GRADES_HASH for grade_int to Font grades
    grades_hash = {
        100: "3", 150: "3+", 200: "4", 250: "4+", 275: "4+", 300: "5",
        350: "5+", 370: "5+", 380: "5+", 400: "6A", 450: "6A+",
        500: "6B", 550: "6B+", 575: "6B+", 600: "6C", 650: "6C+",
        700: "7A", 750: "7A+", 800: "7B", 850: "7B+", 900: "7C",
        950: "7C+", 1000: "8A", 1050: "8A+", 1100: "8B", 1150: "8B+",
        1200: "8C", 1250: "8C+", 1300: "9A", 1350: None, 1400: None,
        1450: None, 1500: None, 0: "?"
    }

    # Update the grade_int column to the corresponding Font grades
    for grade_int, font_grade in grades_hash.items():
        if font_grade is not None:  # Only update if a valid Font grade exists
            cursor.execute(
                "UPDATE crags SET grade_int = ? WHERE grade_int = ?",
                (font_grade, grade_int)
            )


# Main function
def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Call the function to update the Font grades
    font_grading(db_path, cursor, conn)  


    # Commit the changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
    