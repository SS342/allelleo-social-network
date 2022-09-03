def sql_injections_checker(query):
    if "'" in query:
        return True
    return False