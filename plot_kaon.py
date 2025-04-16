import os
import logging
from ROOT import TH1D, TH2D, TFile, TTree, TColor, TCanvas, TLegend, TLatex, TLine, TMath, TEfficiency, TF1, TProfile
from ROOT import kBlack, kBlue, kRed, kYellow, kGreen, kGray, kOrange
from ROOT import gStyle, gPad
from ROOT import gROOT
from ROOT import TStyle
from optparse import OptionParser
import itertools
from math import *
from array import array


def check_output_directory(output_path):
    # checks if output directory exists; if not, mkdir
    if not os.path.exists(str(output_path)):
        os.makedirs(output_path)


# Options
parser = OptionParser()
parser.add_option("-i", "--inFile",   dest='inFile',
                  default="histos_kaon.root", help="Name of the ROOT file")
(options, args) = parser.parse_args()

# Load files
fFile = TFile(options.inFile, "READ")

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

arrBins_E = array('d', (0., 5., 10., 15., 20., 25., 40., 60., 80., 100., 200., 300., 400., 500., 750., 1000.))
arrBins_theta = array('d', (0., 30.*TMath.Pi()/180., 40.*TMath.Pi()/180., 50.*TMath.Pi()/180., 60.*TMath.Pi()/180., 70.*TMath.Pi()/180.,
                            90.*TMath.Pi()/180., 110.*TMath.Pi()/180., 120.*TMath.Pi()/180., 130.*TMath.Pi()/180., 140.*TMath.Pi()/180., 150.*TMath.Pi()/180., TMath.Pi()))

h_reco_E = TH1D('kaon_reco_E', 'kaon_reco_E', len(arrBins_E)-1, arrBins_E)
h_truth_E = TH1D('kaon_truth_E', 'kaon_truth_E', len(arrBins_E)-1, arrBins_E)

h_reco_theta = TH1D('kaon_reco_theta', 'kaon_reco_theta', len(arrBins_theta)-1, arrBins_theta)
h_truth_theta = TH1D('kaon_truth_theta', 'kaon_truth_theta', len(arrBins_theta)-1, arrBins_theta)

tree = fFile.Get("kaon_tree")
for entry in tree:

    h_truth_E.Fill(entry.E_truth)
    h_truth_theta.Fill(entry.theta_truth)
    if entry.E_jet > 0.:
        h_reco_E.Fill(entry.E_truth)
        h_reco_theta.Fill(entry.theta_truth)

c0 = TCanvas("", "", 800, 600)
h_frame = TH1D('framec3', 'framec3', len(arrBins_E)-1, arrBins_E)
 
# Efficiency vs E
eff_rec = TEfficiency(h_reco_E, h_truth_E)
eff_rec.SetLineWidth(2)
eff_rec.SetLineColor(kRed)

h_frame.SetLineColor(kBlack)
h_frame.SetLineWidth(2)
h_frame.SetTitle("")
h_frame.GetYaxis().SetTitle("PFO reconstruction efficiency")
h_frame.GetYaxis().SetTitleOffset(1.2)
h_frame.GetXaxis().SetTitleOffset(1.2)
h_frame.GetXaxis().SetRangeUser(0., 1000)
h_frame.GetXaxis().SetTitle("True neutron E [GeV]")
h_frame.SetMinimum(0.)
h_frame.SetMaximum(1.05)

h_frame.Draw()
eff_rec.Draw("E0SAME")
t2_3 = TLatex()
t2_3.SetTextFont(42)
t2_3.SetTextColor(1)
t2_3.SetTextSize(0.035)
t2_3.SetTextAlign(12)
t2_3.SetNDC()
t2_3.DrawLatex(.62, 0.31, 'Neutron particle gun')
#t2_3.DrawLatex(.62, 0.25, 'Variable cell threshold')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
#t3.DrawLatex(0.15, 0.94, 'Background hits overlay in [-0.5, 15] ns range')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

c0.SaveAs("kaon_efficiency_vs_E.pdf")

# Efficiency vs theta
h_frame2 = TH1D('framec', 'framec', len(arrBins_theta)-1, arrBins_theta)

c = TCanvas("", "", 800, 600)

eff_rec = TEfficiency(h_reco_theta, h_truth_theta)
eff_rec.SetLineColor(kRed)
eff_rec.SetLineWidth(2)

h_frame2.SetLineColor(kBlack)
h_frame2.SetLineWidth(2)
h_frame2.SetTitle("")
h_frame2.GetYaxis().SetTitle("PFO reconstruction efficiency")
h_frame2.GetYaxis().SetTitleOffset(1.2)
h_frame2.GetXaxis().SetTitleOffset(1.2)
h_frame2.GetXaxis().SetRangeUser(0., TMath.Pi())
h_frame2.GetXaxis().SetTitle("True neutron #theta [rad]")
h_frame2.SetMinimum(0.)
h_frame2.SetMaximum(1.05)

h_frame2.Draw()
eff_rec.Draw("E0SAME")

t2_3.DrawLatex(.62, 0.31, 'Neutron particle gun')
#t2_3.DrawLatex(.62, 0.25, 'Variable cell threshold')
#t3.DrawLatex(0.15, 0.94, 'Background hits overlay in [-0.5, 15] ns range')
t4.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

c.SaveAs("kaon_efficiency_vs_theta.pdf")


fFile.Close()
