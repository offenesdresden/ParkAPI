def file_is_allowed(file):
    return file.endswith(".py") and "__Init__" not in file.title() and "Sample_City" not in file.title()
