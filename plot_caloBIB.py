import os
import logging
from ROOT import TH1D, TFile, TTree, TColor, TCanvas, TLegend, TLatex, TLine
from ROOT import kBlack, kBlue, kRed, kYellow, kGreen, kGray, kOrange
from ROOT import gStyle, gPad
from ROOT import gROOT
from ROOT import TStyle
from optparse import OptionParser
import itertools
from math import *


def compose_plot(histname, titleX, titleY, fFileA, fFileB, rminA, stepA, rminB, stepB, rangeX=None):

    c = TCanvas("", "", 800, 600)

    # this is v1
    histA = fFileA.Get(histname)
    histA.SetDirectory(0)

    # this is v0A
    histB = fFileB.Get(histname)
    histB.SetDirectory(0)

    # hardcoding energy normalisation
    r = rminA
    h_barrelA = 2210*2.
    for bin in range(1, histA.GetNbinsX()):
        surface = 2.*pi*r*h_barrelA
        elayer = histA.GetBinContent(bin)
        print(elayer, surface)
        r = r + stepA
        histA.SetBinContent(bin, elayer*1000/(surface/100))

    histA.SetLineColor(kBlue+1)
    histA.SetLineWidth(2)
    histA.SetTitle("")
    histA.GetYaxis().SetTitle(titleY)
    histA.GetYaxis().SetTitleOffset(1.7)
    if rangeX:
        histA.GetXaxis().SetRangeUser(rangeX[0], rangeX[1])
    histA.GetXaxis().SetLabelSize(0.04)
    histA.GetXaxis().SetTitleOffset(1.3)
    histA.GetXaxis().SetTitle(titleX)
    histA.Draw("HIST")

    # hardcoding energy normalisation
    r = rminB
    h_barrelB = 2307*2.
    for bin in range(1, histB.GetNbinsX()):
        surface = 2.*pi*r*h_barrelB
        elayer = histB.GetBinContent(bin)
        print(elayer, surface)
        r = r + stepB
        histB.SetBinContent(bin, elayer*1000/(surface/100))

    histB.SetLineColor(kRed+1)
    histB.SetLineWidth(2)
    histB.Draw("HISTSAME")

    gPad.RedrawAxis()

    leg = TLegend(.5, .5, .8, .65)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    leg.AddEntry(histA, "MuColl v1", "L")
    leg.AddEntry(histB, "#it{MAIA} Detector Concept", "L")

    return c, leg


def check_output_directory(output_path):
    # checks if output directory exists; if not, mkdir
    if not os.path.exists(str(output_path)):
        os.makedirs(output_path)


# Load files, hardcoding FTW...
fFileA = TFile(
    "simhit_v1.root", "READ")
fFileB = TFile(
    "simhit_MAIA.root", "READ")

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

# ECAL barrel
c1, leg = compose_plot(
    "ECAL_simhit_layer", "Calorimeter layer", "Simulated hit energy density [MeV/cm^{2}]", fFileA, fFileB, 1500, 5.05, 1857, 5.35, [0, 50])

leg.Draw()

t2_3 = TLatex()
t2_3.SetTextFont(42)
t2_3.SetTextColor(1)
t2_3.SetTextSize(0.035)
t2_3.SetTextAlign(12)
t2_3.SetNDC()
#t2_3.DrawLatex(.6, 0.84, 'FLUKA 10 TeV BIB simulation')
#t2_3.DrawLatex(.62, 0.85, 'Simulated hits')

t1 = TLatex()
t1.SetTextFont(42)
t1.SetTextColor(1)
t1.SetTextSize(0.04)
t1.SetTextAlign(12)
t1.SetNDC()
t1.DrawLatex(0.5, 0.85, '#bf{#it{Muon Collider}}')

t1_2 = TLatex()
t1_2.SetTextFont(42)
t1_2.SetTextColor(1)
t1_2.SetTextSize(0.04)
t1_2.SetTextAlign(12)
t1_2.SetNDC()
t1_2.DrawLatex(0.5, 0.8, 'Simulation, with BIB (Lattice v0.4)')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.5, 0.74, '#sqrt{s} = 10 TeV')

c1.SaveAs("BIB_ECAL_eloss.pdf")

# Gun energy
# c2, leg = compose_plot("HCAL_simhit_layer", "Calorimeter layer [0.6 #lambda_{0}]", "Energy deposit per layer [GeV]", fFileA, fFileB, 1771, 5, 1771, 5, [0, 75])
# leg.Draw()
# t2_3.DrawLatex(.62, 0.84, 'Photon particle gun')
# c2.SaveAs("BIB_HCAL_eloss.pdf")

fFileA.Close()
fFileB.Close()
