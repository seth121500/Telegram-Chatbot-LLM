import datetime
import requests
from translate import Translator
from Vox import speak


def translate_text(text):
    target_language = 'ja'
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation
