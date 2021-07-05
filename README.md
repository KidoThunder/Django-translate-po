# translate-po

Simple quick script for automatically translating .po files using Google. It speeds up internationalization by giving
translators machine translated base version to correct.

## Usage

Installation

```cmd
pip install django-translate_po
```

Usage with translate function

```python
from translate_po.translator_functions import select_translator_function

# Can use AWS or Google translate service,
# but if want use AWS service, you must add some settings into django's settings.py file, like this:
AWS_TRANSLATE_SERVICE = {
    "service_name": "translate",
    "service_region": "us-west-2",
    "access_key": "your-access-key",
    "access_secret": "your-access_secret"
}
translator_function = select_translator_function("AWS")
# translator_function = select_translator_function("Google")
res_text = translator_function("your-text", source_code="us", target_code="de")
```

Usage with translate po file

```python
from translate_po.translate import PoTranslator

po_translator = PoTranslator("./a.po", translator_service="AWS", source_code="en", target_code="zh")
po_translator.generate_text_for_untranslated()

```

### Changelog

0.1.0

- Release Django-translate_po