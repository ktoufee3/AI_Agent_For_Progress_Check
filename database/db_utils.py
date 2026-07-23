# database/db_utils.py
from database.db_manager import get_connection
from psycopg2.extras import RealDictCursor


# def calculate_project_progress(project_id):

#     conn = get_connection()

#     try:
#         cur = conn.cursor()

#         cur.execute("""
#             SELECT status
#             FROM project_modules
#             WHERE project_id = %s
#         """, (project_id,))

#         modules = cur.fetchall()

#         if not modules:
#             return 0

#         total = 0

#         for (status,) in modules:

#             if status == "Completed":
#                 total += 100

#             elif status == "In Progress":
#                 total += 50

#             elif status == "Not Started":      # Not Started
#                 total += 0

#         progress = round(total / len(modules))

#         cur.execute("""
#             UPDATE projects
#             SET
#                 overall_progress = %s,
#                 updated_at = NOW()
#             WHERE id = %s
#         """, (progress, project_id))

#         conn.commit()

#         return progress

#     finally:
#         cur.close()
#         conn.close()


def get_git_status(project_id):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT
                branch,
                last_processed_commit,
                last_checked_at
            FROM project_git_status
            WHERE project_id = %s
        """, (project_id,))

        row = cur.fetchone()

        if row is None:
            return None

        return {
            "branch": row[0],
            "last_processed_commit": row[1],
            "last_checked_at": (
                row[2].isoformat()
                if row[2] else None
            )
        }

    finally:
        cur.close()
        conn.close()


def initialize_git_tracking(project_id, branch, initial_commit_hash):

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
            initial_commit_hash
        ))

        conn.commit()

    finally:
        cur.close()
        conn.close()



def update_git_status(project_id, last_processed_commit):

    try:

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(
            """
            UPDATE project_git_status
            SET
                last_processed_commit = %s,
                last_checked_at = NOW()
            WHERE project_id = %s
            """,
            (
                last_processed_commit,
                project_id
            )
        )

        conn.commit()

        return {"success": True}

    except Exception as e:

        conn.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        cur.close()
        conn.close()

# def update_project_analysis(
#         project_id,
#         analysis,
#         latest_commit,
#         commits
#     ):

#         conn = get_connection()


#         try:

#             cur = conn.cursor()

#             modules = analysis.get("modules", [])


#             for module in modules:

#                 status = normalize_status(
#                             module["status"]
#                         )

#                 cur.execute("""
#                     UPDATE project_modules
#                     SET
#                         status = %s,
#                         progress = %s,
#                         updated_at = NOW()
#                     WHERE
#                         project_id = %s
#                     AND
#                         module_name = %s
#                 """,
#                 (
#                     status,
#                     module["progress"],
#                     project_id,
#                     module["module_name"]
#                 ))

#                 print("Rows updated:", cur.rowcount)
#                 print(repr(module["module_name"]))

#             # update overall progress

#             overall_progress = calculate_overall_progress(modules)

#             conn.commit()

#             return {
#                 "success": True
#             }


#         except Exception as e:

#             conn.rollback()

#             return {
#                 "success": False,
#                 "error": str(e)
#             }


#         finally:

#             cur.close()
#             conn.close()

def update_project_analysis(project_id, analysis):

    conn = get_connection()

    try:
        cur = conn.cursor()

        modules = analysis.get("modules", [])

        for module in modules:

            status = normalize_status(module["status"])

            cur.execute("""
                UPDATE project_modules
                SET
                    status = %s,
                    progress = %s,
                    updated_at = NOW()
                WHERE
                    project_id = %s
                AND
                    module_name = %s
            """, (
                status,
                module["progress"],
                project_id,
                module["module_name"]
            ))

        # overall_progress = calculate_overall_progress(modules)

        # cur.execute("""
        #     UPDATE projects
        #     SET
        #         overall_progress = %s,
        #         updated_at = NOW()
        #     WHERE id = %s
        # """, (
        #     overall_progress,
        #     project_id
        # ))

        conn.commit()

        return {"success": True}

    except Exception as e:

        conn.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        cur.close()
        conn.close()

def calculate_overall_progress(modules):
    """
    Calculate the overall project progress from module progress.

    Args:
        modules (list): List of module dictionaries containing
                        a 'progress' key.

    Returns:
        float: Overall progress percentage rounded to 2 decimals.
    """

    if not modules:
        return 0.0

    total_progress = sum(
        float(module.get("progress", 0))
        for module in modules
    )

    return round(
        total_progress / len(modules),
        2
    )

def normalize_status(status):

        status = status.strip().lower()

        mapping = {
            "in_progress": "In Progress",
            "in progress": "In Progress",
            "completed": "Completed",
            "complete": "Completed",
            "updated": "In Progress",
            "started": "In Progress",
            "ongoing": "In Progress",
            "working": "In Progress",
            "not_started": "Not Started",
            "not started": "Not Started",
        }

        return mapping.get(
            status.lower(),
            status
        )


def save_commits(
        cur,
        project_id,
        commits
    ):
        """
        Save newly discovered remote commits.
        Existing commits are ignored.
        """

        print(f"saving commits: ...")

        for commit in commits:

            print("Saving: ", commit)

            cur.execute(
                """
                INSERT INTO project_commits
                (
                    project_id,
                    commit_hash,
                    author,
                    commit_date,
                    commit_message
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON CONFLICT (commit_hash)
                DO NOTHING
                """,
                (
                    project_id,
                    commit["commit_hash"],
                    commit["author"],
                    commit["commit_date"],
                    commit["commit_message"]
                )
            )
            print("Rows inserted: ", cur.rowcount)

        print(f"Inserted: ", commit['commit_hash'])

def get_project_modules(project_id):

    conn = get_connection()

    try:

        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            """
            SELECT
                module_name,
                status,
                progress
            FROM project_modules
            WHERE project_id = %s
            ORDER BY id
            """,
            (project_id,)
        )

        return [
            dict(row)
            for row in cur.fetchall()
        ]

    finally:

        cur.close()
        conn.close()

def get_project(project_id=None):
    """
    Return project information.

    If project_id is None, return the first project.
    """

    conn = get_connection()

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if project_id is None:

            cur.execute("""
                SELECT
                    id,
                    project_name,
                    description,
                    repository_url,
                    created_at,
                    updated_at
                FROM projects
                ORDER BY id
                LIMIT 1
            """)

        else:

            cur.execute("""
                SELECT
                    id,
                    project_name,
                    description,
                    repository_url,
                    created_at,
                    updated_at
                FROM projects
                WHERE id = %s
            """, (project_id,))

        project = cur.fetchone()

        if project is None:
            return None

        return dict(project)

    finally:
        cur.close()
        conn.close()


from database.db_manager import get_connection


def get_last_commit(project_id):
    """
    Return the most recent commit for the given project.

    Returns:
        dict | None
    """

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                commit_hash,
                author,
                commit_date,
                commit_message
            FROM project_commits
            WHERE project_id = %s
            ORDER BY commit_date DESC
            LIMIT 5
            """,
            (project_id,)
        )

        row = cur.fetchone()

        if row is None:
            return None

        return {
            "commit_hash": row[0],
            "author": row[1],
            "commit_date": row[2].isoformat() if row[2] else None,
            "commit_message": row[3]
        }

    finally:

        cur.close()
        conn.close()

def run_git(self, args):
    result = subprocess.run(
        ["git", "-C", str(self.project_path)] + args,
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()

def get_latest_commit(self):

    output = self.run_git([
        "log",
        "-1",
        "--pretty=format:%H|%an|%aI|%s"
    ])

    commit_hash, author, date, message = output.split("|", 3)

    return {
        "success": True,
        "commit": {
            "commit_hash": commit_hash,
            "author": author,
            "commit_date": date,
            "commit_message": message
        }
    }

def get_changed_files(self, commit_hash="HEAD"):

    output = self.run_git([
        "diff-tree",
        "--no-commit-id",
        "--name-only",
        "-r",
        commit_hash
    ])

    return {
        "success": True,
        "commit_hash": commit_hash,
        "files": [
            line
            for line in output.splitlines()
            if line.strip()
        ]
    }


