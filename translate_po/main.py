import argparse
import os

import polib

from utilities.constants import UNTRANSLATED_PATH, TRANSLATED_PATH, LANGUAGE_SOURCE, LANGUAGE_DESTINATION, TRANSLATOR
from utilities.io import read_lines, save_lines
from utilities.match import recognize_po_file
from translators.google.translator import GoogleTranslator
from translators.aws.translator import AWSTranslator


def select_translator(source_code, target_code, translator_name):
    class TranslatorSelectorDecorator(object):
        TranslatorSelectors = {}

        def __init__(self, _translator_name):
            self.translator_name = _translator_name

        def __call__(self, function):
            self.TranslatorSelectors[self.translator_name] = function
            return function

    @TranslatorSelectorDecorator(_translator_name="AWS")
    def aws_selector(_target_code, _source_code):
        return AWSTranslator(_target_code, source_code=_source_code).translate

    @TranslatorSelectorDecorator(_translator_name="Google")
    def google_selector(_target_code, _source_code):
        return GoogleTranslator(_target_code, source_code=_source_code).translate

    return TranslatorSelectorDecorator.TranslatorSelectors[translator_name](target_code, source_code)


def translate(source: str, translator_function) -> str:
    """ Translates a single string into target language. """
    return translator_function(source)


def create_close_string(line: str) -> str:
    """ Creates single .po file translation target sting. """
    return r"msgstr " + '"' + line + '"' + "\n"


def solve(new_file: str, old_file: str, translator_function):
    """ Translates single file. """
    lines = read_lines(old_file)
    for line in lines:
        result_text = translate(
            polib.escape(line.msgid), translator_function
        )
        if result_text:
            line.msgstr = polib.unescape(
                result_text
            )
            print(f"Translated {line.msgid} successful.")
        else:
            print(f"Translated {line.msgid} failed")
    save_lines(new_file, lines)


def run(**kwargs):
    """ Core process that translates all files in a directory.
     :parameter fro:
     :parameter to:
     :parameter src:
     :parameter dest:
     """
    found_files = False

    parser = argparse.ArgumentParser(description='Automatically translate PO files using Google translate.')
    parser.add_argument('--fro', type=str, help='Source language you want to translate from to (Default: en)',
                        default=kwargs.get('fro', LANGUAGE_SOURCE))
    parser.add_argument('--to', type=str, help='Destination language you want to translate to (Default: et)',
                        default=kwargs.get('to', LANGUAGE_DESTINATION))
    parser.add_argument('--src', type=str, help='Source directory or the files you want to translate',
                        default=kwargs.get('src', UNTRANSLATED_PATH))
    parser.add_argument('--dest', type=str, help='Destination directory you want to translated files to end up in',
                        default=kwargs.get('dest', TRANSLATED_PATH))
    parser.add_argument('--translator', type=str, help='Translator engine you want to use',
                        default=kwargs.get('translator', TRANSLATOR))
    arguments = parser.parse_args()

    translator_function = select_translator(arguments.fro, arguments.to, arguments.translator)

    for file in os.listdir(arguments.src):
        if recognize_po_file(file):
            found_files = True
            solve(
                os.path.join(arguments.dest, file),
                os.path.join(arguments.src, file),
                translator_function
            )

    if not found_files:
        raise Exception(f"Couldn't find any .po files at: '{arguments.src}'")


if __name__ == '__main__':
    run()
