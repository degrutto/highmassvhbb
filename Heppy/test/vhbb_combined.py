#! /usr/bin/env python

from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# If vhbb_combined is imported from vhbb_combined_data than the next
# line will have no effect (as vhbb is already imported there)
from vhbb import *

from HighMassVHbbAnalysis.Heppy.AdditionalBTag import AdditionalBTag
from HighMassVHbbAnalysis.Heppy.AdditionalBoost import AdditionalBoost
from HighMassVHbbAnalysis.Heppy.GenHFHadronMatcher import GenHFHadronMatcher


# Add Boosted Information
boostana=cfg.Analyzer(
    verbose=False,
    class_object=AdditionalBoost,
)
boostana.GT = "Summer15_25nsV6_DATA" # we do L2L3 for MC and L2L3Res for data. Can therefor use data GT for both
boostana.jecPath = os.environ['CMSSW_BASE']+"/src/HighMassVHbbAnalysis/Heppy/data/jec"
boostana.isMC = sample.isMC
boostana.skip_ca15 = True
sequence.insert(sequence.index(HighMassVHbb),boostana)


genhfana=cfg.Analyzer(
    verbose=False,
    class_object=GenHFHadronMatcher,
)
sequence.insert(sequence.index(HighMassVHbb),genhfana)


treeProducer.collections["ak08"] = NTupleCollection("FatjetAK08ungroomed",  ak8FatjetType,  10,
                                                    help = "AK, R=0.8, pT > 200 GeV, no grooming, calibrated")


#treeProducer.collections["cleanAK08JetsAll"] = NTupleCollection("FatjetCleanAK08ungroomed",  ak8FatjetType,  10,
#                                                  help = "AK, R=0.8, pT > 200 GeV, no grooming, calibrated")



treeProducer.collections["ak08pruned"] = NTupleCollection("FatjetAK08pruned",
                                                            fourVectorType,
                                                            10,
                                                            help="AK, R=0.8, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2, uncalibrated")

treeProducer.collections["ak08prunedcal"] = NTupleCollection("FatjetAK08prunedCal",
                                                             fourVectorType,
                                                             10,
                                                             help="AK, R=0.8, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2, calibrated")


treeProducer.collections["ak08prunedreg"] = NTupleCollection("FatjetAK08prunedReg",
                                                             fourVectorType,
                                                             10,
                                                             help="AK, R=0.8, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2, calibrated and regressed")


treeProducer.collections["ak08prunedsubjets"] = NTupleCollection("SubjetAK08pruned",
                                                                 subjetType,
                                                                 10,
                                                                 help="Subjets of AK, R=0.8, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2")

treeProducer.collections["ak0softdropsubjets"] = NTupleCollection("SubjetAK08softdrop",
                                                                 patSubjetType,
                                                                 10,
                                                                 help="Subjets of AK, R=0.8 softdrop")

if not boostana.skip_ca15:
    treeProducer.collections["ca15ungroomed"] = NTupleCollection("FatjetCA15ungroomed",  fatjetType,  10,
                                                                 help = "CA, R=1.5, pT > 200 GeV, no grooming")

    treeProducer.collections["ca15softdrop"] = NTupleCollection("FatjetCA15softdrop",
                                                                fourVectorType,
                                                                10,
                                                                help="CA, R=1.5, pT > 200 GeV, softdrop zcut=0.1, beta=0")

    # four-vector + n-subjettiness
    treeProducer.collections["ca15softdropz2b1"] = NTupleCollection("FatjetCA15softdropz2b1",
                                                                    fatjetTauType,
                                                                    10,
                                                                    help="CA, R=1.5, pT > 200 GeV, softdrop zcut=0.2, beta=1")

    treeProducer.collections["ca15trimmed"] = NTupleCollection("FatjetCA15trimmed",
                                                                fourVectorType,
                                                                10,
                                                                help="CA, R=1.5, pT > 200 GeV, trimmed r=0.2, f=0.06")

    treeProducer.collections["ca15pruned"] = NTupleCollection("FatjetCA15pruned",
                                                                fourVectorType,
                                                                10,
                                                                help="CA, R=1.5, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2")

    treeProducer.collections["ca15prunedsubjets"] = NTupleCollection("SubjetCA15pruned",
                                                                     subjetType,
                                                                     10,
                                                                     help="Subjets of AK, R=1.5, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2")

    treeProducer.collections["httCandidates"] = NTupleCollection("httCandidates",
                                                                 httType,
                                                                 10,
                                                                 help="OptimalR HEPTopTagger Candidates")


# # Add b-Tagging Information
# 
btagana=cfg.Analyzer(
    verbose=False,
    class_object=AdditionalBTag,
)
sequence.insert(sequence.index(HighMassVHbb),btagana)

# Add Information on generator level hadronic tau decays
if sample.isMC:   
    from HighMassVHbbAnalysis.Heppy.TauGenJetAnalyzer import TauGenJetAnalyzer
    TauGenJet = cfg.Analyzer(
        verbose = False,
        class_object = TauGenJetAnalyzer,
    )
    sequence.insert(sequence.index(HighMassVHbb),TauGenJet)

    treeProducer.collections["tauGenJets"] = NTupleCollection("GenHadTaus", genTauJetType, 15, help="Generator level hadronic tau decays")

# Run Everything
preprocessor = CmsswPreprocessor("combined_cmssw.py", options = {"isMC":sample.isMC})
config.preprocessor=preprocessor
if __name__ == '__main__':
    from PhysicsTools.HeppyCore.framework.looper import Looper 
    looper = Looper( 'Loop', config, nPrint = 1, nEvents = 1000)
    import time
    import cProfile
    p = cProfile.Profile(time.clock)
    p.runcall(looper.loop)
    p.print_stats()
    looper.write()
