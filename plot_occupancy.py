import os
import logging
from ROOT import TH1D, TFile, TTree, TColor, TCanvas, TLegend, TLatex, TLine
from ROOT import kBlack, kBlue, kRed, kYellow, kGray, kOrange
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
parser.add_option('-o', '--outTag', help='--outTag _MAIA',
                  type=str, default='_MAIA')
(options, args) = parser.parse_args()

# Init the logger for the script and various modules
fFile = TFile(options.inFile, "READ")

# Define features here
h_all = fFile.Get('h_nhits')
h_time = fFile.Get('h_ntimehits')

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

c1 = TCanvas("", "", 800, 600)

h_all.SetLineColor(kBlue+1)
h_all.SetFillColor(kBlue+1)
h_all.SetTitle("")
h_all.GetYaxis().SetTitle("Average number of hits / cm^{  2}")
h_all.GetYaxis().SetTitleOffset(1.3)
h_all.SetMaximum(30000)
h_all.SetMinimum(1)
#h_all.GetXaxis().SetNdivisions(10)
h_all.GetXaxis().SetLabelSize(0)
h_all.GetXaxis().SetTitleOffset(0.9)
h_all.GetXaxis().SetTitle("Tracking Detector Layer")
h_all.Draw("HIST")

#print("Bin 0", fFile.Get('h_nhits_nowei').GetBinContent(1))

h_time.SetLineColor(kYellow+1)
h_time.SetFillColor(kYellow+1)
h_time.Draw("HISTSAME")

c1.SetLogy()
gPad.RedrawAxis()

is_ten_TeV = 3
detector_boundaries = [8-is_ten_TeV, 24-is_ten_TeV, 27 - is_ten_TeV, 41-is_ten_TeV, 44-is_ten_TeV]
for bound in detector_boundaries:
    splitLine = TLine(bound, 0, bound, 600)
    splitLine.SetLineWidth(2)
    splitLine.SetLineStyle(2)
    splitLine.SetLineColor(kGray+1)
    splitLine.DrawClone("same")

leg = TLegend(.68, .7, .99, .87)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(h_all, "[-0.5, 15] ns", "F")
leg.AddEntry(h_time, "[-3#sigma_{t}, 5#sigma_{t}]", "F")
leg.Draw()

t1 = TLatex()
t1.SetTextFont(42)
t1.SetTextColor(1)
t1.SetTextSize(0.04)
t1.SetTextAlign(12)
t1.SetNDC()
t1.DrawLatex(0.2, 0.85, '#bf{#it{Muon Collider}}')

t1_2 = TLatex()
t1_2.SetTextFont(42)
t1_2.SetTextColor(1)
t1_2.SetTextSize(0.04)
t1_2.SetTextAlign(12)
t1_2.SetNDC()
t1_2.DrawLatex(0.2, 0.8, 'Simulation, with BIB+IPP (EU24 Lattice)')

t2 = TLatex()
t2.SetTextFont(42)
t2.SetTextColor(kOrange+10)
t2.SetTextSize(0.035)
t2.SetTextAlign(12)
t2.SetTextAngle(90)
t2.SetNDC()
t2.DrawLatex(0.165, 0.485, 'VXD Barrel')
t2.DrawLatex(0.25, 0.45, 'VXD Endcaps')
t2.DrawLatex(0.51, 0.527, 'IT Barrel')
t2.DrawLatex(0.56, 0.485, 'IT Endcaps')
t2.DrawLatex(0.785, 0.51, 'OT Barrel')
t2.DrawLatex(0.84, 0.47, 'OT Endcaps')

t2_2 = TLatex()
t2_2.SetTextFont(42)
t2_2.SetTextColor(1)
t2_2.SetTextSize(0.035)
t2_2.SetTextAlign(12)
t2_2.SetNDC()
#t2_2.DrawLatex(0.48, 0.79, '#sigma_{t}^{IT, OT} = 60 ps')

#t2_3 = TLatex()
#t2_3.SetTextFont(42)
#t2_3.SetTextColor(1)
#t2_3.SetTextSize(0.035)
#t2_3.SetTextAlign(12)
#t2_3.SetNDC()
#t2_3.DrawLatex(0.48, 0.73, 'B_{solenoid} = 5 T')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
t3.DrawLatex(0.69, 0.94, '#it{MAIA} Detector Concept')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.2, 0.74, '#sqrt{s} = 10 TeV')

c1.SaveAs("TrackerOccupancy"+options.outTag+".pdf")

# Define features here
h_all_2D = fFile.Get('h_nhits_endcap_L3_2D')

c2 = TCanvas("", "", 800, 800)
c2.SetTopMargin(0.1)
c2.SetRightMargin(0.1)
c2.SetBottomMargin(0.15)
c2.SetLeftMargin(0.1)

h_all_2D.SetLineColor(kBlue+1)
h_all_2D.SetFillColor(kBlue+1)
h_all_2D.SetTitle("")
h_all_2D.GetYaxis().SetTitle("y [mm]")
h_all_2D.GetYaxis().SetTitleOffset(1.4)
h_all_2D.GetXaxis().SetTitleOffset(1.2)
h_all_2D.GetXaxis().SetTitle("x [mm]")
h_all_2D.Draw("COLZ")

gPad.RedrawAxis()

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
t3.DrawLatex(0.11, 0.94, 'Background hits overlay in [-0.5, 15] ns range')
t3.DrawLatex(0.14, 0.85, 'Vertex Endcap Layer 3')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.78, 0.94, '#sqrt{s} = 10 TeV')

c2.SaveAs("TrackerEndcapOccupancy_2D"+options.outTag+".pdf")

# Define features here
h_endcap_R = fFile.Get('h_nhits_endcap_L3_R')
h_endcap_R_time = fFile.Get('h_nhits_endcap_L3_R_time')

c3 = TCanvas("", "", 800, 600)
c3.SetTopMargin(0.1)
c3.SetRightMargin(0.05)
c3.SetBottomMargin(0.15)
c3.SetLeftMargin(0.15)

h_endcap_R.SetLineColor(kBlue+1)
h_endcap_R.SetFillColor(kBlue+1)
h_endcap_R.SetTitle("")
h_endcap_R.GetYaxis().SetTitle("Average number of hits / cm^{  2}")
h_endcap_R.GetYaxis().SetTitleOffset(1.6)
h_endcap_R.GetXaxis().SetRangeUser(31., 114.)
h_endcap_R.GetXaxis().SetTitleOffset(1.2)
h_endcap_R.GetXaxis().SetTitle("Endcap radius [mm]")
h_endcap_R.Scale(1./2)  #  /2. two sides
h_endcap_R.Draw("HIST")

h_endcap_R_time.SetLineColor(kYellow+1)
h_endcap_R_time.SetFillColor(kYellow+1)
h_endcap_R_time.Scale(1./2)  # /2. accounts for the two sides
h_endcap_R_time.Draw("HISTSAME")

gPad.RedrawAxis()

t1 = TLatex()
t1.SetTextFont(42)
t1.SetTextColor(1)
t1.SetTextSize(0.04)
t1.SetTextAlign(12)
t1.SetNDC()
t1.DrawLatex(0.19, 0.85, '#bf{#it{Muon Collider}}')

t1_2 = TLatex()
t1_2.SetTextFont(42)
t1_2.SetTextColor(1)
t1_2.SetTextSize(0.04)
t1_2.SetTextAlign(12)
t1_2.SetNDC()
t1_2.DrawLatex(0.19, 0.8, 'Simulation, with BIB+IPP (EU24 Lattice)')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
#t3.DrawLatex(0.11, 0.94, 'Background hits overlay in [-0.5, 15] ns range')
t3.DrawLatex(0.67, 0.84, 'Vertex Endcap Layer 3')
t3.DrawLatex(0.7, 0.94, '#it{MAIA} Detector Concept')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.19, 0.74, '#sqrt{s} = 10 TeV')

leg = TLegend(.67, .63, .95, .8)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(h_endcap_R, "[-0.5, 15] ns", "F")
leg.AddEntry(h_time, "[-3#sigma_{t}, 5#sigma_{t}]", "F")
leg.Draw()

c3.SaveAs("TrackerEndcapOccupancy_R"+options.outTag+".pdf")

# Define features here
h_barrel_z = fFile.Get('h_nhits_barrel_L0_z')
h_barrel_z_time = fFile.Get('h_nhits_barrel_L0_z_time')

c4 = TCanvas("", "", 800, 600)
c4.SetTopMargin(0.1)
c4.SetRightMargin(0.05)
c4.SetBottomMargin(0.15)
c4.SetLeftMargin(0.15)

h_barrel_z.SetLineColor(kBlue+1)
h_barrel_z.SetFillColor(kBlue+1)
h_barrel_z.SetTitle("")
h_barrel_z.GetYaxis().SetTitle("Average number of hits / cm^{  2}")
h_barrel_z.GetYaxis().SetTitleOffset(1.6)
h_barrel_z.GetXaxis().SetRangeUser(-65., 65.)
h_barrel_z.GetXaxis().SetTitleOffset(1.2)
h_barrel_z.GetXaxis().SetTitle("Barrel z [mm]")
h_barrel_z.SetMinimum(0)
h_barrel_z.Draw("HIST")
#print("Integral", h_barrel_z.Integral())

h_barrel_z_time.SetLineColor(kYellow+1)
h_barrel_z_time.SetFillColor(kYellow+1)

#h_barrel_z_time.Scale(100.)  # *100. mm2 --> cm2
h_barrel_z_time.Draw("HISTSAME")

gPad.RedrawAxis()

t1 = TLatex()
t1.SetTextFont(42)
t1.SetTextColor(1)
t1.SetTextSize(0.04)
t1.SetTextAlign(12)
t1.SetNDC()
t1.DrawLatex(0.18, 0.85, '#bf{#it{Muon Collider}}')

t1_2 = TLatex()
t1_2.SetTextFont(42)
t1_2.SetTextColor(1)
t1_2.SetTextSize(0.04)
t1_2.SetTextAlign(12)
t1_2.SetNDC()
t1_2.DrawLatex(0.18, 0.8, 'Simulation, with BIB+IPP (EU24 Lattice)')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
#t3.DrawLatex(0.11, 0.94, 'Background hits overlay in [-0.5, 15] ns range')
t3.DrawLatex(0.67, 0.84, 'Vertex Barrel Layer 0')
t3.DrawLatex(0.7, 0.94, '#it{MAIA} Detector Concept')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.18, 0.74, '#sqrt{s} = 10 TeV')

leg = TLegend(.67, .66, .96, .8)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(h_endcap_R, "[-0.5, 15] ns", "F")
leg.AddEntry(h_time, "[-3#sigma_{t}, 5#sigma_{t}]", "F")
leg.Draw()

c4.SaveAs("TrackerBarrelOccupancy_z"+options.outTag+".pdf")

fFile.Close()
