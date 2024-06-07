import argparse
from pprint import pprint
import utils
import os


def check(file_name=None, save=False):
    folder_path = './cache'
    if file_name:
        cache_path = utils.get_file(folder_path, file_name)
    else:
        cache_path = utils.get_most_recent_file(folder_path)

    if not cache_path:
        print(f"File '{file_name}' not found in {folder_path}.")
        exit(1)

    cache = utils.load_pickle(cache_path)

    if save:
        json_folder = '.' + cache_path.split('.')[1].replace('cache', 'json')
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)
            print(f'[Mkdir] {json_folder}')

    date_course_list = []
    for i, (content, n_tokens) in enumerate(cache, 1):
        date_course = utils.extract_json(content)
        date_course_list.append(date_course)
        if save:
            utils.save_json(date_course, f'{json_folder}/date_course_{i}.json')

    return date_course_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get file path or execute function f if no file name is provided.")
    parser.add_argument('--name', type=str, help='The name of the file to search for in the ./cache directory')

    args = parser.parse_args()
    results = check(file_name=args.name, save=True)

    pprint(results[0])
    