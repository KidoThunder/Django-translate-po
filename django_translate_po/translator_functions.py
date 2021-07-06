from django_translate_po.translators.google.translator import GoogleTranslator
from django_translate_po.translators.aws.translator import AWSTranslator


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

        service = getattr(settings, "AWS_TRANSLATE_SERVICE", None)
        if not service:
            raise Exception("Loss of the AWS translate service config")

        return AWSTranslator(
            service["service_name"], service["service_region"], service["access_key"], service["access_secret"]
        ).translate

    @TranslatorSelectorDecorator(_translator_name="Google")
    def google_selector():
        return GoogleTranslator().translate

    return TranslatorSelectorDecorator.TranslatorSelectors[translator_name]()
