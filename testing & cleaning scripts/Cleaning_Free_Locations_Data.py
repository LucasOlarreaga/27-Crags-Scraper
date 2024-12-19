import sqlite3
import re

def update_sector_based_on_description():
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    
    query = '''
        SELECT url, description
        FROM boulders
        WHERE description LIKE '% boulder at %'
        OR description LIKE '% sport at %'
        OR description LIKE '% traditional at %'
        OR description LIKE '% aid at %'
    '''
    
    c.execute(query)
    rows = c.fetchall()
    
    for row in rows:
        url = row[0]
        description = row[1]
        print(description)
        
        # Extract the sector from the description
        match = re.search(r'\b(?:boulder|sport|traditional|aid) at (.+)', description, re.IGNORECASE)
       
        if match:
            sector = match.group(1).strip()
            
            # Update the sector in the database
            c.execute('''
                UPDATE boulders
                SET sector = ?
                WHERE url = ?
            ''', (sector, url))
    
    conn.commit()
    conn.close()


def update_database_schema():
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    try:
        c.execute('''
            ALTER TABLE boulders ADD COLUMN crag TEXT
        ''')
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e):
            print("Column 'crag' already exists.")
        else:
            raise
    conn.commit()
    conn.close()

# Updating crag column for all records based on URL
def update_crag_for_all_records():
    conn = sqlite3.connect('files/free_climbs.db')
    c = conn.cursor()
    
    query = '''
        SELECT url
        FROM boulders
    '''
    
    c.execute(query)
    rows = c.fetchall()
    
    for row in rows:
        url = row[0]
        
        # Extract the crag name from the URL
        crag_match = re.search(r'/crags/([^/]+)/', url)
        crag = crag_match.group(1).replace('-', ' ').title() if crag_match else None
        
        # Update the crag in the database
        c.execute('''
            UPDATE boulders
            SET crag = ?
            WHERE url = ?
        ''', (crag, url))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # This updates the sector to reflect the correct sector based on 
    # the description, rather than using the boulder name as a sector
    update_sector_based_on_description()

    # Update the database schema to add the crag column
    update_database_schema()

    # Update the crag for all records
    update_crag_for_all_records()