import os.path
from pprint import pprint

DIR_REACT = '/Users/tylerbecks/Documents/analytics/src/web/react'
DIR_APP = '/Users/tylerbecks/Documents/analytics/src/web/app'
DIR_SHARED = '/Users/tylerbecks/Documents/analytics/src/web/shared'

def get_test_line_metrics_for_dirs(dirs):
    metrics = get_file_metrics_for_strategy(dirs, get_tested_lines_metrics)
    print('Line Test')
    print_metric_stats(metrics)

def get_test_file_count_metrics_for_dirs(dirs):
    metrics = get_file_metrics_for_strategy(dirs, get_tested_file_count_metrics)
    print('File Count Test')
    print_metric_stats(metrics)

def get_file_metrics_for_strategy(dirs, metric_strategy):
    total_metrics = {
        'total_count': 0,
        'tested_count': 0,
        'untested_count': 0,
    }
    for dir in dirs:
        dir_metrics = metric_strategy(dir)
        total_metrics['total_count'] += dir_metrics['total_count']
        total_metrics['tested_count'] += dir_metrics['tested_count']
        total_metrics['untested_count'] += dir_metrics['untested_count']

    return total_metrics

def print_metric_stats(metrics):
    print('Total: {:,}'.format(metrics['total_count']))

    tested_percent = metrics['tested_count'] / metrics['total_count'] * 100
    print('Tested: {:,} {:.0f}%'.format(metrics['tested_count'], tested_percent))

    untested_percent = metrics['untested_count'] / metrics['total_count'] * 100
    print('Untested: {:,} {:.0f}%'.format(metrics['untested_count'], untested_percent))

def get_tested_file_count_metrics(dir):
    tested_files, src_files = get_tested_untested_files(dir)
    src_file_counts = {k: 1 for k, v in src_files.items()}
    return get_counts(src_file_counts, tested_files)

def get_tested_lines_metrics(dir):
    tested_files, src_files = get_tested_untested_files(dir)
    src_line_counts = {k: line_count(v) for k, v in src_files.items()}
    return get_counts(src_line_counts, tested_files)

def get_counts(file_values, tested_files):
    total_count = sum(file_values.values())
    tested_count = sum([file_values[k] for k in file_values if k in tested_files])
    untested_count = total_count - tested_count

    return {
        'total_count': total_count,
        'tested_count': tested_count,
        'untested_count': untested_count,
    }

def get_tested_untested_files(dir):
    tested_files = set()
    src_files = {}

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
                src_files[file] = full_path

    return tested_files, src_files

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


get_test_line_metrics_for_dirs([DIR_REACT, DIR_APP, DIR_SHARED])
print('_______________')
get_test_file_count_metrics_for_dirs([DIR_REACT, DIR_APP, DIR_SHARED])
