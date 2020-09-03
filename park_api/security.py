def file_is_allowed(file):
    t = file.endswith(".py")
    t &= "__Init__" not in file.title()
    t &= "Sample_City" not in file.title()
    t &= "Frankfurt" not in file.title() # See offenesdresden/ParkAPI#153
    t &= "Aalborg" not in file.title() # See offenesdresden/ParkAPI#212
    return t
