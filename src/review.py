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

    comments = []

    files_for_regex = []
    for change in changes:
        if re.match(regex_list[0], get_file_name(path_source + '/' + change.get('new_path'))):
            files_for_regex.append(change.get('new_path'))

    lines_to_comment = find_wrong_patterns(files_for_regex, wrong_pattern)

    for line_number, line_data in lines_to_comment.items():
        descr_comment = config['message']
        descr_comment = descr_comment.replace("${LINE_NUMBER}", str(line_number))
        descr_comment = descr_comment.replace("${WRONG_PATTERN}", line_data.replace("\n", ""))
        descr_comment = descr_comment.replace("${RIGHT_PATTERN}", rigth_pattern)

        comments.append(commons.comment_create(
            comment_id=commons.comment_generate_id(path_source+str(line_number)),
            comment_path=path_source,
            comment_description=descr_comment,
            comment_end_line=line_number,
            comment_start_line=line_data,
        ))
    print(comments)
    return comments

def find_wrong_patterns(files_for_regex, wrong_pattern):
    wrong_patterns = {}

    for file in files_for_regex:
        with open(file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if check_wrong_pattern_exists(line, wrong_pattern):
                    wrong_patterns[line_number] = line

    return wrong_patterns

def get_file_name(file_path):
    return os.path.basename(file_path)

def check_wrong_pattern_exists(line, wrong_pattern):
    return line.strip().startswith(wrong_pattern)