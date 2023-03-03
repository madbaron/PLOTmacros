import os
import logging
from ROOT import TH1D, TFile, TTree, TColor, TCanvas, TLegend
from ROOT import kBlack, kBlue, kRed
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
                  default="histos_occupancy.root", help="Name of the ROOT histo file")
(options, args) = parser.parse_args()

# Init the logger for the script and various modules
fFile = TFile(options.inFile, "READ")

# Define features here
h_all = fFile.Get('h_nhits')
h_time = fFile.Get('h_ntimehits')

gStyle.SetOptStat(0)

c1 = TCanvas()

h_all.SetLineColor(kBlack)
h_all.SetLineWidth(2)
h_all.SetTitle("")
h_all.GetYaxis().SetTitle("Average number of hits / cm^{2}")
h_all.GetYaxis().SetTitleOffset(1.2)
#h_all.GetXaxis().SetTitleOffset(1.2)
#h_all.GetXaxis().SetTitle("")
h_all.SetMinimum(0.0001)
h_all.GetXaxis().SetNdivisions(5)
#h_all.GetXaxis().SetBinLabel(1, "VXD Barrel L1 Inner")
#h_all.GetXaxis().SetBinLabel(2, "VXD Barrel L1 Outer")
#h_all.GetXaxis().SetBinLabel(3, "VXD Barrel L2 Inner")
#h_all.GetXaxis().SetBinLabel(4, "VXD Barrel L2 Outer")
#h_all.GetXaxis().SetBinLabel(5, "VXD Barrel L3 Inner")
#h_all.GetXaxis().SetBinLabel(6, "VXD Barrel L3 Outer")
#h_all.GetXaxis().SetBinLabel(7, "VXD Barrel L4 Inner")
#h_all.GetXaxis().SetBinLabel(8, "VXD Barrel L4 Outer")
#h_all.GetXaxis().SetBinLabel(9, "VXD Endcap L1 Side A Inner")
#h_all.GetXaxis().SetBinLabel(10, "VXD Endcap L1 Side A Outer")
#h_all.GetXaxis().SetBinLabel(11, "VXD Endcap L2 Side A Inner")
#h_all.GetXaxis().SetBinLabel(12, "VXD Endcap L2 Side A Outer")
#h_all.GetXaxis().SetBinLabel(13, "VXD Endcap L1 Side B Inner")
#h_all.GetXaxis().SetBinLabel(14, "VXD Endcap L1 Side B Outer")
#h_all.GetXaxis().SetBinLabel(15, "VXD Endcap L2 Side B Inner")
#h_all.GetXaxis().SetBinLabel(16, "VXD Endcap L2 Side B Outer")
#h_all.GetXaxis().SetBinLabel(17, "Inner Tracker L1")
h_all.GetXaxis().SetLabelSize(0.04)
h_all.Draw("HIST")

h_time.SetLineColor(kRed)
h_time.SetLineWidth(2)
h_time.Draw("HISTSAME")

h_all.Draw("HISTSAME")

gPad.RedrawAxis()
gPad.SetTopMargin(0.05)
gPad.SetBottomMargin(0.15)
gPad.SetRightMargin(0.15)
#c1.SetLogy()

leg = TLegend(.45, .62, .77, .83)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(h_all, "All hits", "L")
leg.AddEntry(h_time, "Time of flight filters", "L")
leg.Draw()

c1.SaveAs("TrackerOccupancy.pdf")

fFile.Close()
