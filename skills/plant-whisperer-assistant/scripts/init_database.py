#!/usr/bin/env python3
"""
init_database.py - Initialize Plant Whisperer Assistant database
Creates SQLite database with tables for plants, images, analyses, and recommendations
"""

import sqlite3
import os
import argparse
from datetime import datetime

def create_database(db_path):
    """Create the plant database and all required tables"""

    # Ensure directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Creating database at: {db_path}")

    # Plants table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        species TEXT,
        variety TEXT,
        scientific_name TEXT,
        plant_date DATE,
        location TEXT,
        container_size TEXT,
        soil_type TEXT,
        light_requirements TEXT,
        water_requirements TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Images table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_id INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        capture_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        image_type TEXT,
        angle TEXT,
        notes TEXT,
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
    )
    """)

    # Analyses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_id INTEGER NOT NULL,
        image_id INTEGER,
        analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        analysis_mode TEXT,
        overall_health_score REAL,
        primary_issue TEXT,
        issues_detected TEXT,
        confidence REAL,
        notes TEXT,
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE,
        FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
    )
    """)

    # Nutrient levels table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nutrient_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER NOT NULL,
        nitrogen_status TEXT,
        phosphorus_status TEXT,
        potassium_status TEXT,
        calcium_status TEXT,
        magnesium_status TEXT,
        iron_status TEXT,
        notes TEXT,
        FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
    )
    """)

    # Disease detections table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER NOT NULL,
        disease_name TEXT,
        confidence REAL,
        severity TEXT,
        affected_areas TEXT,
        notes TEXT,
        FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
    )
    """)

    # Pest detections table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pest_detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER NOT NULL,
        pest_name TEXT,
        confidence REAL,
        severity TEXT,
        count_estimated INTEGER,
        notes TEXT,
        FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
    )
    """)

    # Environmental stress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS environmental_stress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER NOT NULL,
        stress_type TEXT,
        severity TEXT,
        cause TEXT,
        notes TEXT,
        FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
    )
    """)

    # Recommendations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER NOT NULL,
        recommendation TEXT NOT NULL,
        category TEXT,
        urgency TEXT,
        effectiveness_score REAL,
        difficulty TEXT,
        cost_estimate TEXT,
        organic BOOLEAN DEFAULT 1,
        implemented BOOLEAN DEFAULT 0,
        implementation_date DATE,
        notes TEXT,
        FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
    )
    """)

    # Alerts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_id INTEGER NOT NULL,
        alert_type TEXT,
        severity TEXT,
        message TEXT,
        acknowledged BOOLEAN DEFAULT 0,
        acknowledged_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
    )
    """)

    # Environmental data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS environmental_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_id INTEGER NOT NULL,
        recording_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL,
        soil_moisture REAL,
        ph_level REAL,
        light_level REAL,
        notes TEXT,
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
    )
    """)

    # Plant species reference table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plant_species (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scientific_name TEXT UNIQUE NOT NULL,
        common_name TEXT,
        family TEXT,
        light_requirements TEXT,
        water_requirements TEXT,
        temperature_range TEXT,
        ph_preference TEXT,
        soil_type_preference TEXT,
        nutrient_requirements TEXT,
        common_diseases TEXT,
        common_pests TEXT,
        days_to_maturity INTEGER,
        hardiness_zones TEXT,
        notes TEXT
    )
    """)

    # Disease reference table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diseases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT,
        symptoms TEXT,
        affected_plants TEXT,
        causes TEXT,
        prevention TEXT,
        treatment TEXT,
        organic_treatment TEXT,
        severity_range TEXT,
        notes TEXT
    )
    """)

    # Pest reference table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT,
        description TEXT,
        damage_description TEXT,
        affected_plants TEXT,
        identification TEXT,
        prevention TEXT,
        treatment TEXT,
        organic_treatment TEXT,
        life_cycle TEXT,
        notes TEXT
    )
    """)

    # Nutrient deficiency reference table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nutrient_deficiencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nutrient TEXT UNIQUE NOT NULL,
        symptoms TEXT,
        affected_plants TEXT,
        causes TEXT,
        correction TEXT,
        organic_correction TEXT,
        severity_range TEXT,
        notes TEXT
    )
    """)

    # Create indexes for better performance
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_plants_name ON plants(name)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_images_plant_id ON images(plant_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_analyses_plant_id ON analyses(plant_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_analyses_date ON analyses(analysis_date)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_alerts_plant_id ON alerts(plant_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_alerts_acknowledged ON alerts(acknowledged)
    """)

    # Create triggers for automatic timestamp updates
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_plants_timestamp
    AFTER UPDATE ON plants
    FOR EACH ROW
    BEGIN
        UPDATE plants SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
    """)

    # Insert default data into reference tables
    insert_default_data(cursor)

    # Commit changes
    conn.commit()

    # Print summary
    print("\nDatabase initialized successfully!")
    print(f"Database location: {db_path}")
    print("\nTables created:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")

    print(f"\nTotal tables: {len(tables)}")

    conn.close()

def insert_default_data(cursor):
    """Insert default data into reference tables"""

    print("\nInserting default reference data...")

    # Insert common nutrient deficiencies
    nutrient_data = [
        ('Nitrogen', 'Overall pale green to yellow leaves, starting with older leaves. Stunted growth.', 'Most plants', 'Depleted soil, poor fertilization, leaching', 'Fish emulsion, blood meal, alfalfa meal', 'Fish emulsion, blood meal, compost tea', 'Mild to severe', 'Mobile nutrient, deficiency shows on older leaves first'),
        ('Phosphorus', 'Dark green or purple leaves, especially older leaves and stems. Poor root development.', 'Most plants', 'Poor soil, insufficient fertilizer, cold soil', 'Bone meal, rock phosphate, fish bone meal', 'Bone meal, rock phosphate', 'Mild to moderate', 'Immobile nutrient'),
        ('Potassium', 'Yellow/brown leaf margins (scorch), weak stems. Poor disease resistance.', 'Most plants', 'Depleted soil, leaching, sandy soil', 'Greensand, kelp meal, wood ash', 'Greensand, kelp meal, compost', 'Mild to severe', 'Mobile nutrient'),
        ('Calcium', 'Blossom end rot (tomatoes), tip burn (lettuce), curled leaves. Distorted new growth.', 'Tomatoes, peppers, lettuce', 'Acidic soil, irregular watering', 'Gypsum, lime (if pH low), eggshell powder', 'Gypsum, compost', 'Moderate to severe', 'Immobile nutrient'),
        ('Magnesium', 'Interveinal chlorosis on older leaves. Green veins with yellow tissue between.', 'Most plants', 'Acidic soil, leaching', 'Epsom salts (magnesium sulfate), dolomite lime', 'Epsom salts, compost', 'Mild to moderate', 'Mobile nutrient'),
        ('Iron', 'Interveinal chlorosis on new growth. Veins remain green, tissue between turns yellow/white.', 'Most plants', 'High pH soil, overwatering', 'Chelated iron, iron sulfate', 'Chelated iron, compost', 'Mild to severe', 'Immobile nutrient'),
    ]

    for data in nutrient_data:
        cursor.execute("""
        INSERT OR IGNORE INTO nutrient_deficiencies (nutrient, symptoms, affected_plants, causes, correction, organic_correction, severity_range, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

    # Insert common diseases
    disease_data = [
        ('Powdery Mildew', 'Fungal', 'White powdery coating on leaves, stems, flowers. Yellowing and leaf drop.', 'Squash, cucumbers, roses, phlox, many vegetables', 'High humidity, moderate temperatures, poor air circulation', 'Good air circulation, resistant varieties, neem oil, sulfur spray', 'Sulfur spray, neem oil, milk spray (1:10)', 'Mild to severe', 'Most common fungal disease in home gardens'),
        ('Downy Mildew', 'Fungal', 'Yellow patches on leaf tops, gray fuzzy growth underneath. Leaf drop.', 'Lettuce, grapes, basil, cucumbers', 'Cool, wet weather, high humidity', 'Avoid overhead watering, good drainage, resistant varieties', 'Copper fungicide, biofungicides (Bacillus subtilis)', 'Moderate to severe', 'Different from powdery mildew'),
        ('Early Blight', 'Fungal', 'Dark concentric rings on leaves, starting from bottom of plant. Yellowing and defoliation.', 'Tomatoes, potatoes, peppers', 'Warm, wet weather, poor air circulation', 'Crop rotation, mulching, resistant varieties', 'Copper fungicide, sulfur, biofungicides', 'Moderate to severe', 'Common in tomatoes'),
        ('Late Blight', 'Fungal', 'Water-soaked lesions, white moldy growth, rapid plant death and spread.', 'Tomatoes, potatoes', 'Cool, wet weather (55-75°F)', 'Resistant varieties, good drainage, avoid overhead watering', 'Copper fungicide (must catch early)', 'Severe', 'Very aggressive, destroy infected plants'),
        ('Root Rot', 'Fungal', 'Yellowing, wilting, brown/black mushy roots. Plant death.', 'Most container plants', 'Overwatering, poor drainage, cool soil', 'Well-draining soil, proper watering, avoid waterlogged conditions', 'Beneficial microbes, improve drainage', 'Severe', 'Difficult to reverse once established'),
    ]

    for data in disease_data:
        cursor.execute("""
        INSERT OR IGNORE INTO diseases (name, type, symptoms, affected_plants, causes, prevention, treatment, organic_treatment, severity_range, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

    # Insert common pests
    pest_data = [
        ('Aphids', 'Chewing/Sucking', 'Small (1-8mm), pear-shaped, green/black/white/pink. Clusters on new growth.', 'Curled leaves, sticky honeydew, sooty mold, stunted growth', 'Most plants', 'Attracted to tender new growth, ant symbiosis', 'Beneficial insects, avoid over-fertilizing', 'Water spray, insecticidal soap, neem oil, ladybugs', 'Water spray, insecticidal soap, neem oil, beneficial insects', 'Nymphs (5-10 days) -> Adults (several weeks)', 'Ants farm them for honeydew'),
        ('Spider Mites', 'Sucking', 'Tiny, red/brown, webbing on plants. Barely visible to naked eye.', 'Stippling (tiny dots), yellowing, leaf drop, fine webbing', 'Most plants, especially in dry conditions', 'Hot, dry conditions, dusty conditions', 'Adequate humidity, avoid broad-spectrum pesticides', 'Water spray (increases humidity), neem oil, predatory mites', 'Water spray, predatory mites', 'Egg (6-21 days) -> Larva (2-5 days) -> Nymph (2-5 days) -> Adult (several weeks)', 'Not true spiders'),
        ('Whiteflies', 'Sucking', 'Tiny white moth-like insects, fly when disturbed. Cloud of whiteflies when shaking plant.', 'Yellowing leaves, sticky honeydew, sooty mold, stunted growth', 'Tomatoes, peppers, cucumbers, many ornamentals, houseplants', 'Greenhouse pests, also outdoors in warm climates', 'Avoid over-fertilizing, beneficial insects, yellow traps', 'Yellow sticky traps, insecticidal soap, neem oil', 'Yellow sticky traps, insecticidal soap, neem oil, beneficial insects', 'Egg (7-10 days) -> Nymph (4-6 days) -> Pupa (2-3 days) -> Adult (2-4 weeks)', 'Related to aphids and mealybugs'),
        ('Caterpillars', 'Chewing', 'Soft-bodied larvae, various sizes and colors. May be hairy or smooth.', 'Chewed leaves, holes in foliage, defoliation, visible droppings (frass)', 'Most vegetables, flowers, trees', 'Moth/butterfly eggs hatch on host plants', 'Row covers, beneficial wasps, handpicking', 'Handpick, Bt (Bacillus thuringiensis), neem oil', 'Handpick, Bt, neem oil, row covers, beneficial insects', 'Egg (several days) -> Larva (2-5 weeks) -> Pupa (1-2 weeks) -> Adult', 'Many different species'),
    ]

    for data in pest_data:
        cursor.execute("""
        INSERT OR IGNORE INTO pests (name, type, description, damage_description, affected_plants, identification, prevention, treatment, organic_treatment, life_cycle, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

    print("Default data inserted successfully!")

def main():
    parser = argparse.ArgumentParser(description='Initialize Plant Whisperer Assistant database')
    parser.add_argument('--database', '-d',
                        default='/opt/plant-whisperer/plants.db',
                        help='Database file path (default: /opt/plant-whisperer/plants.db)')
    parser.add_argument('--force', '-f',
                        action='store_true',
                        help='Force recreate database (will delete existing data)')

    args = parser.parse_args()

    # Check if database exists and force flag is not set
    if os.path.exists(args.database) and not args.force:
        response = input(f"Database already exists at {args.database}. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Database initialization cancelled.")
            return

    # If force, delete existing database
    if args.force and os.path.exists(args.database):
        print(f"Deleting existing database: {args.database}")
        os.remove(args.database)

    # Create database
    create_database(args.database)

if __name__ == '__main__':
    main()
