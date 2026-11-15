import unittest
from src.attention import analyze

class AttentionTests(unittest.TestCase):
    def test_current(self):
        self.assertEqual(analyze('Estou com dor no braço.')['attention'], 'sim')
    def test_negation(self):
        self.assertEqual(analyze('Não estou sentindo dor.')['attention'], 'nao')
    def test_breathing(self):
        self.assertEqual(analyze('Estou com falta de ar.')['attention'], 'sim')
    def test_no_complaint(self):
        self.assertEqual(analyze('Estou confortável.')['attention'], 'nao')
    def test_past(self):
        self.assertEqual(analyze('Ontem senti dor mas agora estou bem.')['attention'], 'contexto_passado')
    def test_mixed_context(self):
        self.assertEqual(analyze('Não sinto dor, mas estou com falta de ar.')['attention'], 'sim')
    def test_artifact_preserves_original(self):
        result=analyze('Ontem sentidor, mas agora estou bem.')
        self.assertEqual(result['attention'], 'contexto_passado')
        self.assertTrue(result['review_notes'])
        self.assertIn('sentidor', result['original_text'])
    def test_empty(self):
        self.assertEqual(analyze('')['attention'], 'nao')

if __name__ == '__main__':
    unittest.main()
