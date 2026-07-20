# database/git_status_updater.py

from database.db_manager import get_connection


def get_git_status(project_id):

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                branch,
                last_processed_commit
            FROM project_git_status
            WHERE project_id = %s
        """, (project_id,))

        row = cur.fetchone()

        if not row:
            return None

        return {
            "branch": row[0],
            "last_processed_commit": row[1]
        }

    finally:
        cur.close()
        conn.close()


def save_processed_commit(project_id, branch, commit_hash):

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO project_git_status
            (
                project_id,
                branch,
                last_processed_commit,
                last_checked_at,
                updated_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                NOW(),
                NOW()
            )

            ON CONFLICT (project_id)
            DO UPDATE SET
                branch = EXCLUDED.branch,
                last_processed_commit = EXCLUDED.last_processed_commit,
                last_checked_at = NOW(),
                updated_at = NOW()
        """, (
            project_id,
            branch,
            commit_hash
        ))

        conn.commit()

    finally:
        cur.close()
        conn.close()


def update_last_processed_commit(project_id, commit_hash):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            UPDATE project_git_status
            SET
                last_processed_commit = %s,
                last_checked_at = NOW(),
                updated_at = NOW()
            WHERE project_id = %s
        """,
        (
            commit_hash,
            project_id
        ))

        conn.commit()

    finally:

        cur.close()
        conn.close()

