import os.path
from pprint import pprint

DIR_REACT = '/Users/tylerbecks/Documents/analytics/src/web/react'
DIR_APP = '/Users/tylerbecks/Documents/analytics/src/web/app'
DIR_SHARED = '/Users/tylerbecks/Documents/analytics/src/web/shared'

def get_test_metrics_for_dirs(dirs):
    total_metrics = {
        'total_line_count': 0,
        'tested_line_count': 0,
        'untested_line_count': 0,
    }
    for dir in dirs:
        dir_metrics = get_test_metrics(dir)
        total_metrics['total_line_count'] += dir_metrics['total_line_count']
        total_metrics['tested_line_count'] += dir_metrics['tested_line_count']
        total_metrics['untested_line_count'] += dir_metrics['untested_line_count']

    print_metric_stats(total_metrics)

def print_metric_stats(metrics):
    print('Total Line Count: {:,}'.format(metrics['total_line_count']))

    tested_percent = metrics['tested_line_count'] / metrics['total_line_count'] * 100
    print('Tested line count: {:,} {:.0f}%'.format(metrics['tested_line_count'], tested_percent))

    untested_percent = metrics['untested_line_count'] / metrics['total_line_count'] * 100
    print('Untested line count: {:,} {:.0f}%'.format(metrics['untested_line_count'], untested_percent))

def get_test_metrics(dir):
    tested_files = set()
    src_file_line_counts = {}

    for path, directories, files in os.walk(dir):
        if should_skip_path(path):
            continue

        for file in files:
            if should_skip_file(file):
                continue

            full_path = os.path.join(path, file)

            if is_test_file(file):
                src_file_name = test_file_to_src_file(file)
                print_warning_if_conflict(src_file_name, tested_files, full_path)
                tested_files.add(src_file_name)
            else:
                src_file_line_counts[file] = line_count(full_path)

    total_line_count = sum(src_file_line_counts.values())
    tested_line_count = sum([src_file_line_counts[k] for k in src_file_line_counts if k in tested_files])
    untested_line_count = total_line_count - tested_line_count

    return {
        'total_line_count': total_line_count,
        'tested_line_count': tested_line_count,
        'untested_line_count': untested_line_count,
    }

def print_warning_if_conflict(src_file_name, tested_files, full_path):
    if src_file_name in tested_files:
        print("""WARNING found file name conflict.
    File: {}
    Full path: {}""".format(src_file_name, full_path))

def line_count(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return len([l for l in lines if len(l.strip())])

def test_file_to_src_file(test_file):
    assert is_test_file(test_file)
    return test_file.replace('.spec.', '.')

def is_test_file(file):
    return '.spec.' in file

def should_skip_path(path):
    SKIPPABLE_PATH_TOKENS = ['react/semantic']
    return any([x in path for x in SKIPPABLE_PATH_TOKENS])

def should_skip_file(file):
    INTERESTING_EXTS = ['.coffee', '.js', '.jsx']
    return not any([file.endswith(ext) for ext in INTERESTING_EXTS])


get_test_metrics_for_dirs([DIR_REACT, DIR_APP, DIR_SHARED])
