#!/usr/bin/env python3
"""
Migration helper script for Alembic
Usage: python migrate.py [command]

Available commands:
- generate: Generate a new migration based on model changes
- upgrade: Apply migrations to database
- downgrade: Rollback migrations
- current: Show current migration version
- history: Show migration history
- stamp: Mark database as being at a specific revision
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a command with the virtual environment activated"""
    if os.path.exists("env/bin/activate"):
        full_cmd = f"source env/bin/activate && {cmd}"
    else:
        full_cmd = cmd
    
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "generate":
        message = input("Migration message: ") if len(sys.argv) < 3 else " ".join(sys.argv[2:])
        return run_command(f'alembic revision --autogenerate -m "{message}"')
    
    elif command == "upgrade":
        target = "head" if len(sys.argv) < 3 else sys.argv[2]
        return run_command(f"alembic upgrade {target}")
    
    elif command == "downgrade":
        target = "-1" if len(sys.argv) < 3 else sys.argv[2]
        return run_command(f"alembic downgrade {target}")
    
    elif command == "current":
        return run_command("alembic current")
    
    elif command == "history":
        return run_command("alembic history")
    
    elif command == "stamp":
        if len(sys.argv) < 3:
            print("Usage: python migrate.py stamp <revision>")
            return 1
        return run_command(f"alembic stamp {sys.argv[2]}")
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        return 1

if __name__ == "__main__":
    sys.exit(main())
