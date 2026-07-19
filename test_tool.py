from SMS_Project_Analyzers.git_analyzer import GitAnalyzer


analyzer = GitAnalyzer()

result = analyzer.get_changed_files()

print(result)