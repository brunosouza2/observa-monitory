import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.preparar_interface import localize_html,MARKER
from src.browser_locale import LOCALE_GUARD

class BrowserLocaleTests(unittest.TestCase):
    def test_metadata_before_application_scripts(self):
        source='<html lang="en"><head><script src="app.js"></script></head><body>Original</body></html>'
        output=localize_html(source)
        self.assertIn('<html lang="pt-BR" translate="no">',output)
        self.assertLess(output.index('notranslate'),output.index('app.js'))
        self.assertIn('<body>Original</body>',output)

    def test_idempotent(self):
        first=localize_html('<html lang="en"><head></head><body></body></html>')
        self.assertEqual(localize_html(first),first)
        self.assertEqual(first.count(MARKER),1)

    def test_unknown_template_rejected(self):
        with self.assertRaises(ValueError):localize_html('<div>No document</div>')

    def test_guard_never_overrides_dom_removal(self):
        self.assertNotIn('removeChild',LOCALE_GUARD)
        self.assertNotIn('prototype',LOCALE_GUARD)
        self.assertIn('translate',LOCALE_GUARD)

if __name__=='__main__':unittest.main()
