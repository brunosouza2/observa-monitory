import hashlib,json,sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.movement_v2 import summarize,FEATURES
from src.reference_model import classify

class ReferenceModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact=json.loads(Path('configs/movement-reference-v2.json').read_text())
        cls.reference=json.loads(Path('configs/movement-references-v2.json').read_text())['PM_001']

    def test_missing_reference_abstains(self):
        self.assertEqual(classify({'features':[1]*len(FEATURES)},self.artifact)['status'],'insuficiente')

    def test_invalid_reference_abstains(self):
        self.assertEqual(classify({'features':[1]*len(FEATURES)},self.artifact,{'features':[float('nan')]*len(FEATURES)})['status'],'insuficiente')

    def test_features_require_complete_visible_interval(self):
        self.assertIsNone(summarize([{'time':0,'valid':False}],0,1)['features'])

    def test_reference_label_is_not_query_label(self):
        sample={'features':self.reference['features'],'expected_deviation':0}
        first=classify(sample,self.artifact,self.reference)
        sample['expected_deviation']=1
        self.assertEqual(first['deviation_score'],classify(sample,self.artifact,self.reference)['deviation_score'])

    def test_v1_frozen_sources_preserved(self):
        artifact=json.loads(Path('configs/movement-model.json').read_text())
        for filename,digest in artifact['frozen_sources'].items():
            self.assertEqual(hashlib.sha256(Path(filename).read_bytes()).hexdigest(),digest,filename)

    def test_support_excluded_from_evaluation(self):
        report=json.loads(Path('reports/v2/reference-metrics.json').read_text())
        supports={(r['video_id'],r['repetition']) for r in report['references'].values()}
        queries={(r['video_id'],r['repetition']) for r in report['predictions']}
        self.assertFalse(supports & queries)
        self.assertEqual(len(supports)+len(queries),134)

    def test_runtime_references_reproduce_evaluation_supports(self):
        from scripts.experimento_referencia import export_references
        report=json.loads(Path('reports/v2/reference-metrics.json').read_text())
        runtime=json.loads(Path('configs/movement-references-v2.json').read_text())
        self.assertEqual(export_references(report['references']),runtime)

    def test_json_export_matches_sklearn(self):
        from scripts.experimento_referencia import create,vector
        report=json.loads(Path('reports/v2/reference-metrics.json').read_text())
        rows=report['predictions'];refs=report['references']
        X=np.array([vector(r['features'],refs[r['person_id']]['features']) for r in rows])
        y=np.array([r['expected_deviation'] for r in rows])
        model=create(report['final_candidate']).fit(X,y)
        scores=[classify(r,self.artifact,refs[r['person_id']])['deviation_score'] for r in rows]
        np.testing.assert_allclose(scores,model.predict_proba(X)[:,1],atol=1e-10)

if __name__=='__main__':unittest.main()
