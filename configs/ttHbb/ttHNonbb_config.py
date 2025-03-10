from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.lib.cut_definition import Cut
from pocket_coffea.lib.cut_functions import get_nObj_min, get_HLTsel, get_nBtagEq
from pocket_coffea.parameters.cuts import passthrough
from pocket_coffea.parameters.histograms import *
from pocket_coffea.parameters.btag import btag_variations
import workflow
from workflow import ttHbbBaseProcessor
from pocket_coffea.lib.columns_manager import ColOut

import cloudpickle
import custom_cut_functions 
cloudpickle.register_pickle_by_value(workflow)
cloudpickle.register_pickle_by_value(custom_cut_functions)

from custom_cut_functions import *
import os
localdir = os.path.dirname(os.path.abspath(__file__))

# Loading default parameters
from pocket_coffea.parameters import defaults
default_parameters = defaults.get_default_parameters()
defaults.register_configuration_dir("config_dir", localdir+"/params")

parameters = defaults.merge_parameters_from_files(default_parameters,
                                                  f"{localdir}/params/object_preselection.yaml",
                                                  f"{localdir}/params/triggers.yaml",
                                                  update=True)


cfg = Configurator(
    parameters = parameters,
    datasets = {
        "jsons": [f"{localdir}/datasets/DATA_SingleMuon.json",
                  f"{localdir}/datasets/backgrounds_MC_TTHtoNonbb_redirector.json",
                  f"{localdir}/datasets/THW_2018_redirector.json",
                  f"{localdir}/datasets/TTToSemiLeptonic_2018_redirector.json",
                  f"{localdir}/datasets/TTTo2L2Nu_2018_redirector.json",
                  f"{localdir}/datasets/TTToHadronic_2018_redirector.json",
                  f"{localdir}/datasets/TTZToQQ_2018_redirector.json",
                  f"{localdir}/datasets/TTZtoLLNuNu_2018_redirector.json",
                  f"{localdir}/datasets/TTWJetsToQQ_2018_redirector.json",
                  f"{localdir}/datasets/TTWJetsToLNu_2018_redirector.json",
                  f"{localdir}/datasets/TTGJets_1_2018_redirector.json",
                  f"{localdir}/datasets/TTGJets_2_2018_redirector.json",
                  f"{localdir}/datasets/WW_2018_redirector.json",
                  f"{localdir}/datasets/ZZ_2018_redirector.json",
                  f"{localdir}/datasets/WZ_2018_redirector.json"
    ],
        "filter" : {
            "samples": ["DATA_SingleMuon",
                        "ttHToNonbb",
                        "THW",
                        "TTToSemiLeptonic",
                        "TTTo2L2Nu",
                        "TTToHadronic",
                        "TTZToQQ",
                        "TTZtoLLNuNu",
                        "TTWJetsToQQ",
                        "TTWJetsToLNu",
                        "TTGJets_1",
                        "TTGJets_2",
                        "WW",
                        "WZ",
                         "ZZ"
],
            "samples_exclude" : [],
            "year": ["2018"]
        }
    },

    workflow = ttHbbBaseProcessor,
    #"DoubleEle","EleMu" JUST MUONS, NEED TO ADD ELECTRON DATA
    skim = [get_nObj_min(1, 200., "FatJet"),
            get_HLTsel(primaryDatasets=["DoubleMu"])], 
    
    preselections = [dilepton_presel,
                     get_nObj_min(2,25,"LeptonGood")],
    categories = {
        "baseline": [passthrough],
        "1b" : [ get_nBtagEq(1, coll="BJetGood")],
        "2b" : [ get_nBtagEq(2, coll="BJetGood")],
        "3b" : [ get_nBtagEq(3, coll="BJetGood")],
        "4b" : [ get_nBtagEq(4, coll="BJetGood")]
    },

    weights = {
        "common": {
            "inclusive": ["genWeight","lumi","XS",
                          "pileup",
                          "sf_ele_reco", "sf_ele_id",
                          "sf_mu_id","sf_mu_iso",
                          "sf_btag", "sf_jet_puId",
                          ],
            "bycategory" : {
            }
        },
        "bysample": {
        }
    },

    variations = {
        "weights": {
            "common": {
                "inclusive": [  "pileup",
                                "sf_ele_reco", "sf_ele_id",
                                "sf_mu_id", "sf_mu_iso", "sf_jet_puId",
                              ],
                "bycategory" : {
                }
            },
        "bysample": {
        }    
        },
    },

    
   variables = {
        **ele_hists(coll="ElectronGood", pos=0),
        **muon_hists(coll="MuonGood", pos=0),
        **count_hist(name="nElectronGood", coll="ElectronGood",bins=3, start=0, stop=3),
        **count_hist(name="nMuonGood", coll="MuonGood",bins=3, start=0, stop=3),
        **count_hist(name="nJets", coll="JetGood",bins=8, start=0, stop=8),
        **count_hist(name="nBJets", coll="BJetGood",bins=8, start=0, stop=8),
        **jet_hists(coll="JetGood", pos=0),
        **jet_hists(coll="JetGood", pos=1),
        **jet_hists(coll="JetGood", pos=2),
        **jet_hists(coll="JetGood", pos=3),
        **jet_hists(coll="JetGood", pos=4),
        **jet_hists(name="bjet",coll="BJetGood", pos=0),
        **jet_hists(name="bjet",coll="BJetGood", pos=1),
        **jet_hists(name="bjet",coll="BJetGood", pos=2),
        **fatjet_hists(name="fatjet",coll="FatJetGood"),
        **fatjet_hists(name="bbfatjetTight",coll="BBFatJetGoodT"),
        **fatjet_hists(name="bbfatjetMedium",coll="BBFatJetGoodM"),
        **fatjet_hists(name="bbfatjetLoose",coll="BBFatJetGoodL"),

       # 2D plots
       "jet_eta_pt_leading": HistConf(
           [
               Axis(coll="JetGood", field="pt", pos=0, bins=40, start=0, stop=1000,
                    label="Leading jet $p_T$"),
               Axis(coll="JetGood", field="eta", pos=0, bins=40, start=-2.4, stop=2.4,
                    label="Leading jet $\eta$"),
           ]
       ),
       "jet_eta_pt_all": HistConf(
           [
               Axis(coll="JetGood", field="pt", bins=40, start=0, stop=1000,
                    label="Leading jet $p_T$"),
               Axis(coll="JetGood", field="eta", bins=40, start=-2.4, stop=2.4,
                    label="Leading jet $\eta$")
           ]
       ),
       

    },
    columns = {
        "common": {},
        "bysample": {
            "ttHToNonbb": {
                "bycategory": {
                    "baseline": [
                        ColOut("JetGood", ["eta","pt","phi","btagDeepFlavB"]),
                        ColOut("FatJetGood", ["eta", "pt", "phi", "mass", "msoftdrop", "tau1", "tau2", "tau3", "tau4", "btagDDBvLV2", "deepTagMD_ZHbbvsQCD", "deepTagMD_ZHccvsQCD", "deepTagMD_HbbvsQCD", "deepTagMD_bbvsLight", "btagHbb"]),
                        ColOut("LeptonGood",["eta","pt","phi","pdgId"]),
                        ColOut("BJetGood", ["eta","pt","phi","btagDeepFlavB"]),
                        ColOut("BBFatJetGoodT", ["eta", "pt", "phi", "mass", "msoftdrop", "tau1", "tau2", "tau3", "tau4", "btagDDBvLV2", "deepTagMD_ZHbbvsQCD", "deepTagMD_ZHccvsQCD", "deepTagMD_HbbvsQCD", "deepTagMD_bbvsLight", "btagHbb"]),
                        ColOut("BBFatJetGoodM", ["eta", "pt", "phi", "mass", "msoftdrop", "tau1", "tau2", "tau3", "tau4", "btagDDBvLV2", "deepTagMD_ZHbbvsQCD", "deepTagMD_ZHccvsQCD", "deepTagMD_HbbvsQCD", "deepTagMD_bbvsLight", "btagHbb"]),
                        ColOut("BBFatJetGoodL", ["eta", "pt", "phi", "mass", "msoftdrop", "tau1", "tau2", "tau3", "tau4", "btagDDBvLV2", "deepTagMD_ZHbbvsQCD", "deepTagMD_ZHccvsQCD", "deepTagMD_HbbvsQCD", "deepTagMD_bbvsLight", "btagHbb"])
                    ]
                }
            }
        }
    }
    
)




run_options = {
        "executor"       : "dask/lxplus",
        "env"            : "singularity",
        "workers"        : 1,
        "scaleout"       : 50,
        "worker_image"   : "/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-analysis/general/pocketcoffea:lxplus-cc7-latest",
        "queue"          : "microcentury",
        "walltime"       : "00:40:00",
        "mem_per_worker" : "4GB", # GB
        "disk_per_worker" : "1GB", # GB
        "exclusive"      : False,
        "chunk"          : 400000,
        "retries"        : 50,
        "treereduction"  : 20,
        "adapt"          : False,
        "skipbadfiles"   : 10
    }
   
