def random_baseline_enron(levels):
    if levels == 2:
        return 0.49
    elif levels == 3:
        return 0.33
    else:
        raise Exception("Unsupported number of levels")