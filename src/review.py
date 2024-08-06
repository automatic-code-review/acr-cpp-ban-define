import automatic_code_review_commons as commons
import os
import re
def review(config):
    merge = config['merge']
    wrong_pattern = config['wrong_pattern']
    rigth_pattern = config['rigth_pattern']
    regex_list = config['regex_list']
    changes = merge['changes']
    path_source = config['path_source']
    path_ignore = config['path_ignore']

    comments = []

    files_for_regex = []
    for change in changes:
        if re.match(regex_list[0], get_file_name(path_source + '/' + change.get('new_path'))):

            ignore_file = False
            for path_to_ignore in path_ignore:
                if re.match(path_ignore[0], get_file_name(path_source + '/' + change.get('new_path'))):
                    ignore_file = True

            if not ignore_file:
                files_for_regex.append(change.get('new_path'))

    wrong_declations = find_wrong_patterns(files_for_regex, wrong_pattern)

    for wrong_declaration in wrong_declations:
        descr_comment = config['message']
        descr_comment = descr_comment.replace("${LINE_NUMBER}", str(wrong_declaration['line_number']))
        descr_comment = descr_comment.replace("${WRONG_PATTERN}", str(wrong_declaration['wrong_pattern']).replace("\n", ""))
        descr_comment = descr_comment.replace("${RIGHT_PATTERN}", rigth_pattern)

        comments.append(commons.comment_create(
            comment_id=commons.comment_generate_id(path_source+str(wrong_declaration['line_number'])),
            comment_path=wrong_declaration['path'],
            comment_description=descr_comment,
            comment_end_line=wrong_declaration['line_number'],
            comment_start_line=wrong_declaration['line_number'],
        ))
    print(comments)
    return comments

def find_wrong_patterns(files_for_regex, wrong_pattern):
    wrong_patterns = []

    for file in files_for_regex:
        with open(file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if check_wrong_pattern_exists(line, wrong_pattern):

                    wrong_declaration = {
                        'line_number': line_number,
                        'wrong_pattern': line,
                        'path': file
                    }

                    wrong_patterns.append(wrong_declaration)

    return wrong_patterns

def get_file_name(file_path):
    return os.path.basename(file_path)

def check_wrong_pattern_exists(line, wrong_pattern):
    return line.strip().startswith(wrong_pattern)