import sqlite3

# Mapping of incorrect country names to correct country names
country_mapping = {
    'Andorra': 'Andorra',
    'Bakersfield, ca': 'United States of America',
    'Bosnia and herzegovina': 'Bosnia and Herz.',
    'Caribbean netherlands': 'Netherlands',
    'Cayman islands': 'Cayman Islands',
    'Chattanooga, tn': 'United States of America',
    'Costa rica': 'Costa Rica',
    'Czech republic': 'Czechia',
    'El salvador': 'El Salvador',
    'Faroe islands': 'Denmark',
    'Gibraltar': 'United Kingdom',
    'Hong kong': 'China',
    'Iran, islamic republic of': 'Iran',
    'Korea republic of': 'South Korea',
    'Korea, republic of': 'South Korea',
    'Macedonia': 'North Macedonia',
    'Malta': 'Malta',
    'Monaco': 'Monaco',
    'Netherlands antilles': 'Netherlands',
    'New zealand': 'New Zealand',
    'North macedonia': 'North Macedonia',
    'Palestinian territory, occupied': 'Palestine',
    'Reunion': 'France',
    'Russian federation': 'Russia',
    'Saudi arabia': 'Saudi Arabia',
    'Seychelles': 'Seychelles',
    'Singapore': 'Singapore',
    'South africa': 'South Africa',
    'Sri lanka': 'Sri Lanka',
    'St george, ut': 'United States of America',
    'Taiwan province of china': 'Taiwan',
    'Tanzania, united republic of': 'Tanzania',
    'United arab emirates': 'United Arab Emirates',
    'United kingdom': 'United Kingdom',
    'United states': 'United States of America',
    'Usa': 'United States of America',
    'Viet nam': 'Vietnam',
    'Virgin islands british': 'United Kingdom',
    'Washington, dc': 'United States of America'
}

# Connect to the database
conn = sqlite3.connect('files/merged_climbs.db')
cursor = conn.cursor()

# Update the countriy column
cursor.execute('''
    UPDATE climbs
    SET country = TRIM(country)
''')

cursor.execute('''
    UPDATE climbs
    SET country = UPPER(SUBSTR(country, 1, 1)) || LOWER(SUBSTR(country, 2))
''')

# Update the country column based on the mapping
for incorrect_name, correct_name in country_mapping.items():
    cursor.execute('''
        UPDATE climbs
        SET country = ?
        WHERE country = ?
    ''', (correct_name, incorrect_name))

# Commit the changes and close the connection
conn.commit()
conn.close()