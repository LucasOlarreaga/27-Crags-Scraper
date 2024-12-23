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
        1200: "8C", 1250: "8C+", 1300: "9A", 1350: "9A+", 1400: "9B",
        1450: "9B+", 1500: "9C", 1550: "9C+", 1600: "10A", 0: "?"
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


#if __name__ == "__main__":
   #main()
    

#------------------------------------------------

# Since I now want the grading for the merged file in V grades, I am converting it back

# Path to SQLite database
db_path = "files/merged_climbs.db"

def font_to_v_grading(cursor):
    # Mapping from Font grades to V grades (as integers)
    font_to_v = {
        # Lowercase grades
        "3": 0, "3+": 0, "4": 1, "4+": 1, "5": 2,
        "5+": 2, "6a": 3, "6a+": 3, "6b": 4, "6b+": 4,
        "6c": 5, "6c+": 5, "7a": 6, "7a+": 7, "7b": 8,
        "7b+": 8, "7c": 9, "7c+": 10, "8a": 11, "8a+": 12,
        "8b": 13, "8b+": 14, "8c": 15, "8c+": 16, "9a": 17,
        "9a+": 18, "9b": 19, "9b+": 20, "9c": 21, "9c+": 22,
        "?": None, 
        # Uppercase grades
        "6A": 3, "6A+": 3, "6B": 4, "6B+": 4,
        "6C": 5, "6C+": 5, "7A": 6, "7A+": 7, "7B": 8,
        "7B+": 8, "7C": 9, "7C+": 10,
        "8B": 13, "8B+": 14, "8C": 15, "8C+": 16, "9A": 17,
        "9A+": 18, "9B": 19, "9B+": 20, "9C": 21, "9C+": 22,
        "?": None, 
    }

    # Update the grade_int column to the corresponding V grades (as integers)
    for font_grade, v_grade in font_to_v.items():
        cursor.execute(
            "UPDATE climbs SET grade = ? WHERE grade = ?",
            (v_grade, font_grade)
            )

     
# Main function
def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Call the function to update the grades from Font to V grades (as integers)
    font_to_v_grading(cursor)

    cursor.execute(
        "SELECT grade FROM climbs WHERE grade > 17",
            )
    

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()   