from time import sleep


def retry(func) -> bool:
    attempts = 5
    attempt = 0
    while True:
        if func():
            break
        else:
            attempt += 1
            if attempt >= attempts:
                raise Exception(f"Operation failed after {attempts}.")
            sleep(1)
            continue


def recursively_replace_value(mydict: dict, key: str, val: str):
    """
    Recursively searches mydict for key and replaces its value (if any) with val
    :param mydict:
    :param key:
    :param val:
    :return:
    """
    if key in mydict:
        mydict[key] = val

    for key2 in mydict:
        value = mydict[key2]
        if isinstance(value, dict):
            recursively_replace_value(value, key, val)
