from googletrans import Translator

from translators.base_translator import TranslatorCacheController, AbstractTranslator


class GoogleTranslator(AbstractTranslator, TranslatorCacheController):
    def __init__(self, target_code, source_code="en"):
        self.source_code = source_code
        self.target_code = target_code
        self.client = Translator()

    def translate(self, text):
        cache_key = self.get_cache_key(text, self.source_code, self.target_code)
        cached_result = self.get_cache(cache_key)
        if cached_result:
            return cached_result

        result_text = self._translate(text)
        if result_text:
            self.set_cache(cache_key, result_text)
            return result_text

    def _translate(self, text):
        try:
            result_text = self.client.translate(text, src=self.source_code, dest=self.target_code).text
        except Exception as e:
            print(f"{e} - Google Translate failed, text:{text}")
            return None
        return result_text

