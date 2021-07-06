import json
import os

from redbaron import RedBaron

FILES_STATUS = {"FAIL": [], "SUCCESS": [], "PASS": []}
RESULT_OUTPUT_PATH = "./result.json"


def has_english_char(string):
    """
    , 44 - 45
    . 46 - 47
    : - ; 58 - 60
    A - Z 65 - 91
    a - z 97 - 123
    """
    string = str(string)

    for char in string:
        for start, end in (
            (44, 45),
            (46, 47),
            (58, 60),
            (65, 91),
            (97, 123),
        ):
            assert start < end
            if start <= ord(char) <= end:
                return True

    return False


def is_aleady_gettext(node):
    parent = node.parent_find("AtomtrailersNode")
    # print(parent.help())
    # print(parent.value)
    if parent is not None:
        for i in parent.value:
            if i.type == "name" and i.value == "_":
                return True
    return False


def is_docstring(node):
    if node.parent is None:
        return False
    if node.parent.parent is None:
        return True
    if node.parent.type in ["class", "def"]:
        return True
    return False


def update_file(py_file_path):
    with open(py_file_path) as f:
        original_code = f.read()

    root = RedBaron(original_code)

    for node in root.find_all("StringNode"):
        if (
            has_english_char(node)
            and not is_aleady_gettext(node)
            and not is_docstring(node)
        ):
            node.replace("_({}) ".format(node))

    modified_code = root.dumps()

    # 有些文件没有以空行结尾，出于尚未明了的原因，redbaron 会在代码末尾加上空行，让脚本误以为代码变化了，所以这里判断一下代码变动的长度
    if original_code != modified_code and len(modified_code) - len(original_code) > 1:
        modified_code = (
            "from django.utils.translation import gettext as _\n" + modified_code
        )
        with open(py_file_path, "w") as f:
            f.write(modified_code)
        return True
    else:
        return False


def walk(dir_path, skip_paths):
    sub_paths = [
        os.path.join(dir_path, i) for i in os.listdir(dir_path) if i not in skip_paths
    ]

    for sub_path in sub_paths:
        if os.path.isdir(sub_path):
            yield from walk(sub_path, skip_paths)
        elif sub_path.endswith(".py"):
            yield sub_path


def main():
    project_paths = [
        './applications'
    ]
    for project_path in project_paths:
        all_py_file_paths = list(
            walk(
                project_path, [
                    "b3report", "invoice_portal", "router", "tests", "scripts", "migrations", "services", "tasks",
                    "unittest_utils", "webhooks", "subscription_transactions", "models_managers"
            ]
            )
        )
        for i, py_file_path in enumerate(all_py_file_paths):
            try:
                print(
                    "{} / {} {} ".format(i, len(all_py_file_paths), py_file_path),
                    end="\r",
                )
                is_changed = update_file(py_file_path)
                if is_changed:
                    FILES_STATUS["SUCCESS"].append(py_file_path)
                else:
                    FILES_STATUS["PASS"].append(py_file_path)
            except Exception as e:
                print("\n error")
                print(e)
                FILES_STATUS["FAIL"].append({"path": py_file_path, "error": str(e)})

        with open(RESULT_OUTPUT_PATH, "w") as f:
            f.write(json.dumps(FILES_STATUS, indent=4))


if __name__ == "__main__":
    main()
