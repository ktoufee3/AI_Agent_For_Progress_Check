from database.project_analysis_updater import ProjectAnalysisUpdater


analysis = {
    "modules": [
        {
            "module_name": "Student Management",
            "changes": [
                "Added Student model"
            ],
            "status": "in_progress",
            "progress": 10
        }
    ]
}



result = ProjectAnalysisUpdater().update(
    project_id=1,
    analysis=analysis,
    commit_hash="3759d243b92201d159a39fd83818865f8086b6f3"
)


print(result)