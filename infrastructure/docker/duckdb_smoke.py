from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[2]
STORAGE_DIR = ROOT / "storage"
DB_PATH = STORAGE_DIR / "analytics.duckdb"


def main() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(DB_PATH)) as conn:
        conn.execute(
            """
            create schema if not exists raw;
            create schema if not exists clean;
            create schema if not exists curated;
            """
        )
        conn.execute(
            """
            create or replace table raw.week1_smoke as
            select
                1 as id,
                'duckdb-ready' as status,
                current_timestamp as checked_at;
            """
        )
        result = conn.execute(
            "select id, status from raw.week1_smoke;"
        ).fetchone()

    print(f"DuckDB smoke test OK: {result[0]} {result[1]}")
    print(f"Database: {DB_PATH}")


if __name__ == "__main__":
    main()
