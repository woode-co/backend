def timer(func):
    """
    To check elasped execution time of given func.
    
    """
    import time

    def sec2timestr(t):
        ms = int(t * 1000) % 1000
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return f"{time_str}.{ms}"
    
    def wrapper(*args, **kwargs):
        st = time.time()
        print(f"[Start Time] ", sec2timestr(st))
        result = func(*args, **kwargs)
        et = time.time()
        print(f"[Finish Time]", sec2timestr(et))
        print(f"Function '{func.__name__}' executed in {et-st:.4f} seconds")
        return result
    return wrapper


def load_pickle(file_path):
    try:
        with open(file_path, 'rb') as file:
            import pickle
            data = pickle.load(file)
    except FileNotFoundError:
        data = {}
    return data


def save_pickle(data, file_path):
    with open(file_path, 'wb') as file:
        import pickle
        pickle.dump(data, file)


def create_file(prefix='', suffix='', extension=''):
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{prefix}{current_time}{suffix}.{extension}"
    return file_path


def get_file(folder_path, file_path):
    import os
    file_path = os.path.join(folder_path, file_path)
    if os.path.exists(file_path):
        return file_path
    else:
        return None


def get_most_recent_file(folder_path):
    import os, glob
    files = glob.glob(os.path.join(folder_path, '*'))
    if not files:
        return None
    most_recent_file = max(files, key=os.path.getmtime)
    return most_recent_file


def extract_json(s):
    import re
    pattern = re.compile(r'```json(.*?)```', re.DOTALL)
    match = pattern.search(s)
    if match:
        return match.group(1).strip()
    else:
        return ""
    

def save_json(json_str, file_path):
    import json
    try:
        json_data = json.loads(json_str)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON data has been saved to {file_path}")
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)