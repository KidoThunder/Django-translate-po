import boto3

from translators.base_translator import TranslatorCacheController, AbstractTranslator

from .aws_config import AWS_CONFIG


class AWSTranslator(AbstractTranslator, TranslatorCacheController):
    def __init__(self, target_code, source_code="en"):
        self.source_code = source_code
        self.target_code = target_code

        self.service_name = AWS_CONFIG["service_name"]
        self.region_name = AWS_CONFIG['region_name']
        self.aws_access_key_id = AWS_CONFIG['aws_access_key_id']
        self.aws_secret_access_key = AWS_CONFIG['aws_secret_access_key']
        self.client = boto3.client(
            service_name=self.service_name,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            use_ssl=True
        )

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
            result = self.client.translate_text(
                Text=text, SourceLanguageCode=self.source_code, TargetLanguageCode=self.target_code
            )
        except Exception as e:
            print(f"{e} - AWS Translate failed, text:{text}")
            return None
        return result.get("TranslatedText", None)
