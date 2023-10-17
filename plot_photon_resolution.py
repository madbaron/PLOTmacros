import os
import logging
from ROOT import TH1D, TH2D, TFile, TTree, TColor, TCanvas, TLegend, TLatex, TLine, TMath, TEfficiency, TF1
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
                  default="ntup_tracks.root", help="Name of the ROOT file")
parser.add_option("-a", "--inAlt",   dest='inAlt',
                  default="ntup_tracks.root", help="Name of the ROOT file")
(options, args) = parser.parse_args()

# Load files
fFile = TFile(options.inFile, "READ")
fFileAlt = TFile(options.inAlt, "READ")

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)


arrBins_theta = array('d', (0., 30.*TMath.Pi()/180., 40.*TMath.Pi()/180., 50.*TMath.Pi()/180., 60.*TMath.Pi()/180., 70.*TMath.Pi()/180.,
                            90.*TMath.Pi()/180., 110.*TMath.Pi()/180., 120.*TMath.Pi()/180., 130.*TMath.Pi()/180., 140.*TMath.Pi()/180., 150.*TMath.Pi()/180., TMath.Pi()))
arrBins_E = array('d', (0., 5., 10., 15., 20., 25., 50.,
                  100., 250., 500., 1000., 2500., 5000.))

h_resolution = TH2D('photon_resolution_theta', 'photon_resolution_theta', len(
    arrBins_theta)-1, arrBins_theta, 100, -400, 200)

tree = fFile.Get("photon_tree")
for entry in tree:
    h_resolution.Fill(entry.theta_truth, entry.E-entry.E_truth)

h_reso_theta = TH1D('reso_theta', 'reso_theta',
                    len(arrBins_theta)-1, arrBins_theta)
for bin in range(0, len(arrBins_theta)-1):
    h_my_proj = h_resolution.ProjectionY("_py", bin, bin+1)
    gaussFit = TF1("gaussfit", "gaus")
    h_my_proj.Fit(gaussFit, "E")
    sigma = gaussFit.GetParameter(2)
    sigma_err = gaussFit.GetParError(2)
    h_reso_theta.SetBinContent(bin+1, sigma/1000.)
    h_reso_theta.SetBinError(bin+1, sigma_err/1000.)

h_resolutionAlt = TH2D('photon_resolution_thetaAlt', 'photon_resolution_thetaAlt', len(
    arrBins_theta)-1, arrBins_theta, 100, -400, 200)

tree = fFileAlt.Get("photon_tree")
for entry in tree:
    h_resolutionAlt.Fill(entry.theta_truth, entry.E-entry.E_truth)

h_reso_thetaAlt = TH1D('reso_thetaAlt', 'reso_thetaAlt',
                       len(arrBins_theta)-1, arrBins_theta)
for bin in range(0, len(arrBins_theta)-1):
    h_my_proj = h_resolutionAlt.ProjectionY("_py", bin, bin+1)
    gaussFit = TF1("gaussfit", "gaus")
    h_my_proj.Fit(gaussFit, "E")
    sigma = gaussFit.GetParameter(2)
    sigma_err = gaussFit.GetParError(2)
    h_reso_thetaAlt.SetBinContent(bin+1, sigma/50.)
    h_reso_thetaAlt.SetBinError(bin+1, sigma_err/50.)

    if bin == 5:
        cdebug = TCanvas("", "", 800, 600)
        # h_resolutionAlt.Draw("COLZ")
        h_my_proj.Draw()
        cdebug.SaveAs("debug.pdf")


c2 = TCanvas("", "", 800, 600)
h_reso_theta.SetTitle(" ")
h_reso_theta.SetLineColor(kBlack)
h_reso_theta.SetLineWidth(2)
h_reso_theta.SetMaximum(1.2)
h_reso_theta.SetMinimum(0.005)
h_reso_theta.GetYaxis().SetTitle("Photon energy resolution #sigma_{E}/E")
h_reso_theta.GetYaxis().SetTitleOffset(1.4)
h_reso_theta.GetXaxis().SetTitleOffset(1.2)
# h_reso_theta.GetXaxis().SetRangeUser(-0.24, 0.5)
h_reso_theta.GetXaxis().SetTitle("Truth photon #theta [rad]")
h_reso_theta.Draw("E0")
h_reso_thetaAlt.SetLineColor(kBlue+1)
h_reso_thetaAlt.SetLineWidth(2)
h_reso_thetaAlt.Draw("E0SAME")

c2.SetLogy()

leg = TLegend(.4, 0.45, .9, 0.55)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(h_reso_thetaAlt, "E_{#gamma} = 50 GeV w/o BIB subtraction", "L")
leg.AddEntry(h_reso_theta, "E_{#gamma} = 50 GeV with BIB subtraction", "L")
leg.Draw()

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()

t3.DrawLatex(0.15, 0.94, 'Background hits overlay in [-0.5, 10] ns range')
t4.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

c2.SaveAs("reso_vs_theta.pdf")

fFile.Close()
