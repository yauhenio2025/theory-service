#!/usr/bin/env python3
"""
Run database migrations for Theory Service.
Can be run manually or as part of deploy process.

Usage:
    python db/migrate.py
"""

import os
import sys
from pathlib import Path

import psycopg2

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/theory_db")

# Convert postgres:// to postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


def run_migrations():
    """Run all SQL migrations in order."""
    migrations_dir = Path(__file__).parent / "migrations"

    if not migrations_dir.exists():
        print("No migrations directory found")
        return

    # Get all .sql files sorted by name
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        print("No migration files found")
        return

    print(f"Found {len(migration_files)} migration(s)")
    print(f"Database: {DATABASE_URL[:50]}...")

    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            for migration_file in migration_files:
                print(f"\nRunning: {migration_file.name}")
                sql = migration_file.read_text()
                cur.execute(sql)
                print(f"  ✓ {migration_file.name} completed")
    except Exception as e:
        print(f"Migration error: {e}")
        sys.exit(1)
    finally:
        conn.close()

    print("\n✓ All migrations completed!")


if __name__ == "__main__":
    run_migrations()
