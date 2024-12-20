import sqlite3

def create_merged_database():
    conn = sqlite3.connect('files/merged_climbs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS climbs (
            id TEXT PRIMARY KEY,
            name TEXT,
            grade TEXT,
            rating REAL,
            ascents INTEGER,
            type TEXT,
            sector TEXT,
            country TEXT,
            crag TEXT,
            origin TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_free_climbs():
    conn_free = sqlite3.connect('files/free_climbs.db')
    conn_merged = sqlite3.connect('files/merged_climbs.db')
    c_free = conn_free.cursor()
    c_merged = conn_merged.cursor()
    
    c_free.execute('SELECT url, name, grade, rating, ascents, type, sector, country, crag FROM boulders')
    rows = c_free.fetchall()
    
    for row in rows:
        c_merged.execute('''
            INSERT OR IGNORE INTO climbs (id, name, grade, rating, ascents, type, sector, country, crag, origin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Free')
        ''', row)
    
    conn_merged.commit()
    conn_free.close()
    conn_merged.close()

def insert_premium_climbs():
    conn_premium = sqlite3.connect('files/premium_climbs.db')
    conn_merged = sqlite3.connect('files/merged_climbs.db')
    c_premium = conn_premium.cursor()
    c_merged = conn_merged.cursor()
    
    c_premium.execute('SELECT id, name, grade_int, rating, ascents_done_count, genre, region, country, crag_name FROM crags')
    rows = c_premium.fetchall()
    
    for row in rows:
        c_merged.execute('''
            INSERT OR IGNORE INTO climbs (id, name, grade, rating, ascents, type, sector, country, crag, origin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Premium')
        ''', row)
    
    conn_merged.commit()
    conn_premium.close()
    conn_merged.close()

def main():
    create_merged_database()
    insert_free_climbs()
    insert_premium_climbs()
    print("Merged database created successfully.")

if __name__ == "__main__":
    main()