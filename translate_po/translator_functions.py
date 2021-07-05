from translators.google.translator import GoogleTranslator
from translators.aws.translator import AWSTranslator


def select_translator_function(translator_name):
    class TranslatorSelectorDecorator(object):
        TranslatorSelectors = {}

        def __init__(self, _translator_name):
            self.translator_name = _translator_name

        def __call__(self, function):
            self.TranslatorSelectors[self.translator_name] = function
            return function

    @TranslatorSelectorDecorator(_translator_name="AWS")
    def aws_selector():
        from django.conf import settings

        aws_translate_service = settings.get("AWS_TRANSLATE_SERVICE")
        if not aws_translate_service:
            raise Exception("Loss of the AWS translate service config")

        return AWSTranslator(
            aws_translate_service["service_name"], aws_translate_service["service_region"],
            aws_translate_service["access_key"], aws_translate_service["access_secret"],
        ).translate

    @TranslatorSelectorDecorator(_translator_name="Google")
    def google_selector():
        return GoogleTranslator().translate

    return TranslatorSelectorDecorator.TranslatorSelectors[translator_name]()
