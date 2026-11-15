import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.movement import angle,measure,summarize,classify,FEATURES,select_person
from src.session import combine,new_session,html_report

class MovementTests(unittest.TestCase):
    def test_angle_and_degenerate(self):
        self.assertAlmostEqual(angle(np.array([0,1]),np.array([0,0]),np.array([1,0])),90)
        self.assertIsNone(angle(np.array([0,0]),np.array([0,0]),np.array([1,0])))
    def test_visibility_abstains(self):
        self.assertIsNone(measure(np.zeros((17,2)),np.zeros(17)))
    def test_insufficient_coverage(self):
        result=summarize([{'time':0,'valid':False}],0,1)
        self.assertIsNone(result['features'])
        self.assertEqual(classify(result,{})['status'],'insuficiente')
    def test_intervals_do_not_use_future(self):
        rows=[{'time':i,'valid':True,'abduction':20 if i<5 else 150,'elbow':180,'trunk':0,'shoulder_asymmetry':0} for i in range(10)]
        self.assertEqual(summarize(rows,0,4)['features'][0],20)
    def test_person_selection_tracks_center(self):
        boxes=np.array([[0,0,100,200],[200,0,220,40]])
        self.assertEqual(select_person(boxes),0)
        self.assertEqual(select_person(boxes,np.array([210,20])),1)
    def test_missing_video_no_normal_claim(self):
        self.assertEqual(combine(None,None)['events'],[])
    def test_unaligned_not_combined(self):
        video={'feature_names':FEATURES,'repetitions':[{'status':'desvio','start':0,'end':2,'features':[1]*6}]}
        audio={'segments':[{'start':0,'end':2,'text':'Sinto dor.'}]}
        self.assertFalse(combine(video,audio,False)['combined'])
        self.assertTrue(combine(video,audio,True)['combined'])
    def test_escaped_export(self):
        session=new_session(audio={'segments':[],'transcript':'<script>alert(1)</script>'})
        output=html_report(session)
        self.assertNotIn('<script>',output)
        self.assertIn('&lt;script&gt;',output)

if __name__=='__main__':unittest.main()
