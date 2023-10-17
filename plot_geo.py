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
                  default="histos_occupancy.root", help="Name of the ROOT histo file")
(options, args) = parser.parse_args()

# Init the logger for the script and various modules
fFile = TFile(options.inFile, "READ")

# Define features here
VXD_xy = fFile.Get('VXD_xy')

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

c1 = TCanvas("", "", 800, 800)

VXD_xy.SetTitle("")
VXD_xy.GetYaxis().SetTitle("y [mm]")
VXD_xy.GetYaxis().SetTitleOffset(1.4)
VXD_xy.GetXaxis().SetLabelSize(0.04)
VXD_xy.GetXaxis().SetTitleOffset(1.4)
VXD_xy.GetXaxis().SetTitle("x [mm]")
VXD_xy.GetXaxis().SetRangeUser(-140., 140.)
VXD_xy.GetYaxis().SetRangeUser(-140., 140.)
VXD_xy.Draw("AP")

gPad.RedrawAxis()

c1.SaveAs("VXD_xy.pdf")

fFile.Close()
