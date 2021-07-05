import polib

from translate_po.translator_functions import select_translator_function


class PoTranslator(object):
    def __init__(self, file_path: str, translator_service="Google", source_code="en", target_code="zh"):
        self.source_code = source_code
        self.target_code = target_code

        self.file_path = file_path
        self.po_file = polib.pofile(file_path)
        self.translate_function = select_translator_function(translator_service)

    @property
    def untranslated_entries(self):
        return self.po_file.untranslated_entries()

    @property
    def po_escape(self):
        return polib.escape

    @property
    def po_unescape(self):
        return polib.unescape

    def generate_text_for_untranslated(self):
        for po_line in self.untranslated_entries:
            translated_text = self.translate_function(
                text=self.po_unescape(po_line.msgid), source_code=self.source_code, target_code=self.target_code
            )
            if not translated_text:
                continue
            po_line.msgstr = self.po_escape(translated_text)
        self.po_file.save(self.file_path)
