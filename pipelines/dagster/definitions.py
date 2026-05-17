import os
import subprocess
from pathlib import Path

from dagster import Definitions, In, Nothing, job, op


WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", "/workspace"))
DBT_PROJECT_DIR = WORKSPACE_ROOT / "pipelines" / "dbt"


def run_command(command: list[str], cwd: Path) -> None:
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = str(DBT_PROJECT_DIR)

    process = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    if process.stdout:
        print(process.stdout)
    if process.stderr:
        print(process.stderr)

    if process.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {process.returncode}: {' '.join(command)}"
        )


@op
def dbt_seed() -> None:
    run_command(["dbt", "seed"], DBT_PROJECT_DIR)


@op(ins={"start": In(Nothing)})
def dbt_run() -> None:
    run_command(["dbt", "run"], DBT_PROJECT_DIR)


@op(ins={"start": In(Nothing)})
def dbt_test() -> None:
    run_command(["dbt", "test"], DBT_PROJECT_DIR)


@job
def analytics_pipeline() -> None:
    dbt_test(dbt_run(dbt_seed()))


defs = Definitions(jobs=[analytics_pipeline])
