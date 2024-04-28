def delete_crops():
    import shutil
    shutil.rmtree('runs', ignore_errors=False, onerror=None)