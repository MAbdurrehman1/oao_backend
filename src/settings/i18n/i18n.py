from pathlib import Path

from utils.i18n import Language, register_translations, set_default_language

_TRANSLATIONS_DIRECTORY = Path(__file__).parent / "yamls"

register_translations(Language.DE, yaml_path=_TRANSLATIONS_DIRECTORY / "de.yaml")
set_default_language(Language.DE)
