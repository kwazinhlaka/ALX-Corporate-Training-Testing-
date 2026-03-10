"""Convert insurance.csv into a SQLite .db file for teaching SQL joins (SQLite).

Usage (VS Code terminal):
    python convert_insurance_to_db.py --csv insurance.csv --db insurance.db

Creates a normalised schema:
- dim_sex, dim_smoker, dim_region
- person
- insurance_fact

Also creates teaching views:
- vw_insurance_flat (CSV-like view)
- vw_*_demo views for INNER/LEFT/RIGHT/FULL OUTER concepts (SQLite emulation)
- vw_cross_join_region_smoker_grid
- vw_self_join_similar_bmi_pairs
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sqlite3
import pandas as pd


def build_db(csv_path: Path, db_path: Path) -> None:
    df = pd.read_csv(csv_path)

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE dim_sex (
      sex_id INTEGER PRIMARY KEY,
      sex TEXT NOT NULL UNIQUE
    );
    CREATE TABLE dim_smoker (
      smoker_id INTEGER PRIMARY KEY,
      smoker TEXT NOT NULL UNIQUE
    );
    CREATE TABLE dim_region (
      region_id INTEGER PRIMARY KEY,
      region TEXT NOT NULL UNIQUE
    );

    CREATE TABLE person (
      person_id INTEGER PRIMARY KEY AUTOINCREMENT,
      age INTEGER NOT NULL,
      bmi REAL NOT NULL,
      children INTEGER NOT NULL,
      sex_id INTEGER NOT NULL,
      smoker_id INTEGER NOT NULL,
      region_id INTEGER NOT NULL,
      FOREIGN KEY (sex_id) REFERENCES dim_sex(sex_id),
      FOREIGN KEY (smoker_id) REFERENCES dim_smoker(smoker_id),
      FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
    );

    CREATE TABLE insurance_fact (
      person_id INTEGER NOT NULL,
      charges REAL NOT NULL,
      FOREIGN KEY (person_id) REFERENCES person(person_id)
    );

    CREATE INDEX idx_person_sex_id ON person(sex_id);
    CREATE INDEX idx_person_smoker_id ON person(smoker_id);
    CREATE INDEX idx_person_region_id ON person(region_id);
    CREATE INDEX idx_fact_person_id ON insurance_fact(person_id);
    """)

    for val in sorted(df["sex"].unique()):
        cur.execute("INSERT INTO dim_sex (sex) VALUES (?)", (val,))
    for val in sorted(df["smoker"].unique()):
        cur.execute("INSERT INTO dim_smoker (smoker) VALUES (?)", (val,))
    for val in sorted(df["region"].unique()):
        cur.execute("INSERT INTO dim_region (region) VALUES (?)", (val,))

    for _, row in df.iterrows():
        sex_id = cur.execute("SELECT sex_id FROM dim_sex WHERE sex=?", (row["sex"],)).fetchone()[0]
        smoker_id = cur.execute("SELECT smoker_id FROM dim_smoker WHERE smoker=?", (row["smoker"],)).fetchone()[0]
        region_id = cur.execute("SELECT region_id FROM dim_region WHERE region=?", (row["region"],)).fetchone()[0]

        cur.execute(
            "INSERT INTO person (age, bmi, children, sex_id, smoker_id, region_id) VALUES (?,?,?,?,?,?)",
            (int(row["age"]), float(row["bmi"]), int(row["children"]), sex_id, smoker_id, region_id),
        )
        pid = cur.lastrowid
        cur.execute("INSERT INTO insurance_fact (person_id, charges) VALUES (?,?)", (pid, float(row["charges"])))

    cur.executescript("""
    CREATE VIEW vw_insurance_flat AS
    SELECT
      p.person_id,
      p.age,
      s.sex,
      p.bmi,
      p.children,
      sm.smoker,
      rg.region,
      f.charges
    FROM person p
    JOIN insurance_fact f ON f.person_id = p.person_id
    JOIN dim_sex s        ON s.sex_id = p.sex_id
    JOIN dim_smoker sm    ON sm.smoker_id = p.smoker_id
    JOIN dim_region rg    ON rg.region_id = p.region_id;

    CREATE VIEW vw_fact_filtered_demo AS
    SELECT * FROM insurance_fact
    WHERE (person_id % 10) != 0;

    CREATE VIEW vw_fact_with_orphans_demo AS
    SELECT person_id, charges FROM insurance_fact
    UNION ALL SELECT 1339, 9999.99
    UNION ALL SELECT 1340, 8888.88
    UNION ALL SELECT 1341, 7777.77
    UNION ALL SELECT 1342, 6666.66
    UNION ALL SELECT 1343, 5555.55;

    CREATE VIEW vw_inner_join_demo AS
    SELECT p.person_id, p.age, f.charges
    FROM person p
    JOIN vw_fact_filtered_demo f ON f.person_id = p.person_id;

    CREATE VIEW vw_left_join_demo AS
    SELECT p.person_id, p.age, f.charges
    FROM person p
    LEFT JOIN vw_fact_filtered_demo f ON f.person_id = p.person_id;

    CREATE VIEW vw_right_join_demo AS
    SELECT f.person_id, p.age, f.charges
    FROM vw_fact_with_orphans_demo f
    LEFT JOIN person p ON p.person_id = f.person_id;

    CREATE VIEW vw_full_outer_join_demo AS
    SELECT p.person_id, p.age, f.charges
    FROM person p
    LEFT JOIN vw_fact_with_orphans_demo f ON f.person_id = p.person_id
    UNION ALL
    SELECT p.person_id, p.age, f.charges
    FROM vw_fact_with_orphans_demo f
    LEFT JOIN person p ON p.person_id = f.person_id
    WHERE p.person_id IS NULL;

    CREATE VIEW vw_cross_join_region_smoker_grid AS
    WITH grid AS (
      SELECT rg.region, sm.smoker
      FROM dim_region rg
      CROSS JOIN dim_smoker sm
    )
    SELECT
      g.region,
      g.smoker,
      COUNT(v.person_id) AS n_people,
      ROUND(AVG(v.charges), 2) AS avg_charges
    FROM grid g
    LEFT JOIN vw_insurance_flat v
      ON v.region = g.region AND v.smoker = g.smoker
    GROUP BY g.region, g.smoker;

    CREATE VIEW vw_self_join_similar_bmi_pairs AS
    SELECT
      p1.person_id AS person_a,
      p2.person_id AS person_b,
      rg.region,
      p1.bmi AS bmi_a,
      p2.bmi AS bmi_b,
      ROUND(ABS(p1.bmi - p2.bmi), 3) AS bmi_diff
    FROM person p1
    JOIN person p2
      ON p1.person_id < p2.person_id
     AND p1.region_id = p2.region_id
     AND ABS(p1.bmi - p2.bmi) <= 0.5
    JOIN dim_region rg ON rg.region_id = p1.region_id;
    """)

    conn.commit()
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=Path("insurance.csv"), help="Path to insurance.csv")
    parser.add_argument("--db", type=Path, default=Path("insurance.db"), help="Output SQLite DB path")
    args = parser.parse_args()
    build_db(args.csv, args.db)
    print(f"✅ Created SQLite database: {args.db.resolve()}")


if __name__ == "__main__":
    main()
