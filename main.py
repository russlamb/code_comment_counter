import os
import re
from collections import namedtuple

ProcessResult = namedtuple('ProcessResult', ['lines', 'comments', 'ratio', 'root'])


def traverse(start_path=".", file_extension="", exclude_files=[]):
    """ traverse root directory, and process files"""
    process_results = []
    for root, dirs, files in os.walk(start_path):
        path = root.split(os.sep)
        fs_files = [f for f in files if
                    f.endswith(file_extension) and f not in exclude_files]  # get all files with extension
        result = process_files(fs_files, root)
        process_results.append(result)

    return process_results


def get_comment_ratio(start_path=".", file_extension="", exclude_files=[]):
    results = traverse(start_path, file_extension, exclude_files)
    total_lines = 0
    total_comments = 0
    for result in results:
        total_lines += result.lines
        total_comments += result.comments
    total_ratio = 0 if total_lines == 0 else total_comments / total_lines
    return ProcessResult(total_lines, total_comments, total_ratio, start_path)


def number_of_lines_in_file(filepath):
    """Get number of lines in file"""

    try:
        num_lines = sum(1 for line in open(filepath, "r"))
    except Exception as e:
        num_lines = 0
    return num_lines


def number_of_comments(filepath, comment_style="fsharp"):
    """Return number of comments"""
    try:
        with open(filepath) as f:
            content = f.read()
            if comment_style == "fsharp":
                comment_regex = r"(//[^\n]*\n)|(\(\*+[^*]*\*+(?:[^/*][^*]*\*+)*\))"
            else:
                comment_regex = r"(//[^\n]*\n)|(/\*+[^*]*\*+(?:[^/*][^*]*\*+)*/)"

            regex = re.compile(  # this regex checks single line comments "//" or multiline comments for F# e.g. "(* *)"
                comment_regex)
            # for C# style comments use (//[^\n]*\n)|(/\*+[^*]*\*+(?:[^/*][^*]*\*+)*/)
            result = regex.findall(content)
            return len(result)
    except Exception as e:
        pass

    return 0


def process_files(fs_files, root):
    """process files"""
    # print_root(fs_files, path, root)
    # print_file_name(fs_files, path)
    (lines, comments, comment_line_ratio) = (0, 0, 0)
    for f in fs_files:
        file_path = os.path.join(root, f)
        lines = number_of_lines_in_file(file_path)
        comments = number_of_comments(file_path)
        comment_line_ratio = 0 if lines == 0 else comments / lines
    if len(fs_files) > 0:
        print("{} comments:{} lines:{} ratio:{:.2f}".format(root, comments, lines, comment_line_ratio))
    return ProcessResult(lines, comments, comment_line_ratio, root)


def print_root(fs_files, path, root):
    """print directory path if there are any matching files"""
    if len(fs_files) > 0:  # check if the directory contains any matching files
        print((len(path) - 1) * '---', os.path.basename(root))  # print the path


def print_file_name(fs_files, path):
    """print files"""
    for file in fs_files:  # print the matching file names
        print(len(path) * '---', file)


if __name__ == "__main__":
    process_result = get_comment_ratio(r"C:\source", ".fs", ["AssemblyInfo.fs"])
    print("FSharp lines:{} comments:{} ratio:{}".format(process_result.lines, process_result.comments,
                                                        process_result.ratio))
    process_result = get_comment_ratio(r"C:\source", ".cs", ["AssemblyInfo.cs"])
    print("CSharp lines:{} comments:{} ratio:{}".format(process_result.lines, process_result.comments,
                                                        process_result.ratio))
