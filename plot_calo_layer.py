import os
import logging
from ROOT import TH1D, TFile, TTree, TColor, TCanvas, TLegend, TLatex, TLine
from ROOT import kBlack, kBlue, kRed, kYellow, kGray
from ROOT import gStyle, gPad
from ROOT import gROOT
from ROOT import TStyle
from optparse import OptionParser
import itertools
from math import fabs


def check_output_directory(output_path):
    # checks if output directory exists; if not, mkdir
    if not os.path.exists(str(output_path)):
        os.makedirs(output_path)


# Options
parser = OptionParser()
parser.add_option("-i", "--inFile",   dest='inFile',
                  default="ntup_calo.root", help="Name of the ROOT histo file")
(options, args) = parser.parse_args()

# Init the logger for the script and various modules
fFile = TFile(options.inFile, "READ")

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

# ECAL
h_ECALbarrel = fFile.Get('ECAL_hit_layer_barrel')
h_HCALbarrel = fFile.Get('HCAL_hit_layer_barrel')

c3 = TCanvas("", "", 800, 600)
c3.SetLogy()

h_ECALbarrel.SetLineColor(kRed)
h_ECALbarrel.SetLineWidth(2)
h_ECALbarrel.SetTitle("")
h_ECALbarrel.GetYaxis().SetTitle("Energy density [GeV / mm^{  2}]")
h_ECALbarrel.GetYaxis().SetTitleOffset(1.7)
h_ECALbarrel.SetMinimum(0.000000001)
h_ECALbarrel.SetMaximum(h_ECALbarrel.GetMaximum()*2.)
h_ECALbarrel.GetXaxis().SetRangeUser(0, 75)
h_ECALbarrel.GetXaxis().SetNdivisions(10)
h_ECALbarrel.GetXaxis().SetLabelSize(0.04)
h_ECALbarrel.GetXaxis().SetTitleOffset(1.3)
h_ECALbarrel.GetXaxis().SetTitle("Calorimeter layer")
h_ECALbarrel.Draw("HIST")

h_HCALbarrel.SetLineColor(kBlue+1)
h_HCALbarrel.SetLineWidth(2)
h_HCALbarrel.Draw("HISTSAME")

gPad.RedrawAxis()

leg = TLegend(.7, .7, .9, .84)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(h_ECALbarrel, "BIB in ECAL", "L")
leg.AddEntry(h_HCALbarrel, "BIB in HCAL", "L")
leg.Draw()

t2 = TLatex()
t2.SetTextFont(42)
t2.SetTextColor(1)
t2.SetTextSize(0.035)
t2.SetTextAlign(12)
t2.SetNDC()
t2.DrawLatex(0.2, 0.24, 'Calorimeter Barrel')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
t3.DrawLatex(0.15, 0.94, 'Background hits overlay in [-0.5, 10] ns range')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

c3.SaveAs("TotalCALOccupancy.pdf")

fFile.Close()
