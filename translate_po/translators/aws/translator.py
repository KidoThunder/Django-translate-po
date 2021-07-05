import boto3

from translators.base_translator import TranslatorCacheController, AbstractTranslator


class AWSTranslator(AbstractTranslator, TranslatorCacheController):
    def __init__(self, translate_service_name, aws_region_name, aws_access_key, aws_access_secret):
        self.client = boto3.client(
            service_name=translate_service_name,
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_access_secret,
            use_ssl=True
        )

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
            result = self.client.translate_text(
                Text=text, SourceLanguageCode=source_code, TargetLanguageCode=target_code
            )
        except Exception as e:
            print(f"{e} - AWS Translate failed, text:{text}")
            return None
        return result.get("TranslatedText", None)
