import automatic_code_review_commons as commons
import os
import re
def review(config):
    merge = config['merge']
    wrong_pattern = config['wrongPattern']
    rigth_pattern = config['rigthPattern']
    regexList = config['regexFile']
    changes = merge['changes']

    comments = []

    filesForRegex = []
    for change in changes:
        if re.match(regexList[0], getFileName(change.get('new_path'))):
            #TODO verificar se o arquivo vai vir no path_source ou new_path
            filesForRegex.append(change.get('new_path'))

    lines_to_comment = findWrongPattern(filesForRegex, wrong_pattern)

    for key, value in lines_to_comment.items():
        descr_comment = config['message']
        descr_comment = descr_comment.replace("${LINE_NUMBER}", str(key))
        descr_comment = descr_comment.replace("${WRONG_PATTERN}", value.replace("\n", ""))
        descr_comment = descr_comment.replace("${RIGHT_PATTERN}", rigth_pattern)

        comments.append(commons.comment_create(
            comment_id=commons.comment_generate_id(descr_comment),
            #TODO pegar o path do arquivo
            comment_path="",
            comment_description=descr_comment,
            comment_end_line=key,
            comment_start_line=key,
        ))

    return comments

def findWrongPattern(filesForRegex, wrongPattern):
    defines = {}

    for file in filesForRegex:
        with open(file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if checkDefineExists(line, wrongPattern):
                    defines[line_number] = line

    return defines
def getFileName(filePath):
    return os.path.basename(filePath)

def checkDefineExists(line, wrong_pattern):
    return line.strip().startswith(wrong_pattern)