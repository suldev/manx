verbose = False

def section(message):
    print(f":: {message}")

def info(message):
    print (f"II {message}")

def warn(message):
    print (f"WW {message}")

def error(message):
    print (f"EE {message}")

def fatal(message):
    print (f"FF {message}")
    quit()

def debugstop(message):
    print (f"DS {message}")
    quit()

def debug(message):
    if verbose:
        print (f"DD {message}")