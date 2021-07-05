from googletrans import Translator

from translators.base_translator import TranslatorCacheController, AbstractTranslator


class GoogleTranslator(AbstractTranslator, TranslatorCacheController):
    def __init__(self):
        self.client = Translator()

    def translate(self, text, target_code, source_code="en"):
        cache_key = self.get_cache_key(text, source_code, target_code)
        cached_result = self.get_cache(cache_key)
        if cached_result:
            return cached_result

        result_text = self._translate(text, source_code, target_code)
        if result_text:
            self.set_cache(cache_key, result_text)
            return result_text

    def _translate(self, text, source_code, target_code):
        try:
            resp = self.client.translate(text, src=source_code, dest=target_code)
            result_text = resp.text
        except Exception as e:
            print(f"{e} - Google Translate failed, text:{text}")
            return None
        return result_text
