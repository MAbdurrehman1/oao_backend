from __future__ import annotations
import logging
from enum import Enum
from functools import cache, singledispatch
from pathlib import Path
from typing import Any

from yaml import safe_load, YAMLError

from cexceptions import AbstractException

logger = logging.getLogger(name="i18n")


class Language(str, Enum):
    EN = "EN"
    DE = "DE"

    @classmethod
    def from_code(cls, code: str) -> Language:
        return cls(code.upper())


class TranslationRegistry:
    _lang_to_path: dict[Language, Path] = {}
    default_lang: Language | None = None

    @classmethod
    def register(cls, lang: Language, yaml_path: Path) -> None:
        cls._lang_to_path[lang] = yaml_path
        logger.info(f"Registered Path({yaml_path}) for Language({lang}).")

    @classmethod
    def register_multiple(cls, lang_to_path: dict[Language, Path]) -> None:
        for lang, yaml_path in lang_to_path.items():
            cls.register(lang, yaml_path)

    @classmethod
    def read_translations(cls, lang: Language) -> dict[str, str]:
        if lang not in cls._lang_to_path:
            logger.warning(f"No translation file registered for Language({lang}).")
            return {}

        filepath = cls._lang_to_path[lang]
        return cls._read_translations(filepath)

    @classmethod
    @cache
    def _read_translations(cls, filepath: Path) -> dict[str, str]:
        try:
            with open(filepath, "r") as yaml:
                return safe_load(yaml)
        except FileNotFoundError:
            logger.warning(f"Translation file at Path{filepath} not found.")
        except YAMLError as e:
            logger.warning(
                f"Parsing translation file at Path({filepath}) failed with "
                f"exception: {e}"
            )

        return {}

    @classmethod
    def set_default_language(cls, lang: Language):
        cls.default_lang = lang
        logger.info(f"Set default language to Language({lang}).")


def register_translations(lang: Language, yaml_path: Path) -> None:
    TranslationRegistry.register(lang, yaml_path)


def set_default_language(lang: Language) -> None:
    TranslationRegistry.default_lang = lang


@singledispatch
def translate(x: Any, lang: Language | None = None):
    raise NotImplementedError(f"'translate' not implemented for type({type(x)}).")


@translate.register
def _(x: str, lang: Language | None = None) -> str:
    lang = lang or TranslationRegistry.default_lang

    if not lang:
        logger.warning("No default language set.")
        return x

    translations: dict = TranslationRegistry.read_translations(lang)

    translation: str | None = translations.get(x)

    if not translation:
        logger.warning(f"Translation not found for key({x}) in Language({lang}).")
        return x

    return translation


@translate.register
def _(xs: list, lang: Language | None = None) -> list:
    return [translate(x, lang) for x in xs]


@translate.register
def _(xs: set, lang: Language | None = None) -> set:
    return {translate(x, lang) for x in xs}


@translate.register
def _(e: Exception, lang: Language | None = None) -> Exception:
    message: str = translate(str(e), lang)
    return type(e)(message)


@translate.register
def _(e: AbstractException, lang: Language | None = None) -> AbstractException:
    message: str = translate(e.message, lang)
    return e.replace(message=message)
