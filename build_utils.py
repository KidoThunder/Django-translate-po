import argparse
import glob
import os


def generate_docs():
    os.system("pdoc --html translate_po.main --force --output-dir ./docs")


def delete_files_in_directory(directory):
    files = glob.glob(directory)
    for file in files:
        os.remove(file)


def build_dist():
    os.system("python setup.py sdist bdist_wheel")


def upload_to_pypi(live=False):
    if live:
        os.system(f"twine upload dist/*")
    else:
        os.system(f"twine upload -r testpypi dist/*")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-live', type=bool, default=False)
    arguments = parser.parse_args()

    print("### Generating documentation")
    generate_docs()
    print("### Cleaning distributable directory")
    delete_files_in_directory("./dist/*")
    print("### Building the distributable")
    build_dist()
    print("### Uploading the distributable to PyPi")
    upload_to_pypi(live=arguments.live)
    print("### Distributable uploaded")
