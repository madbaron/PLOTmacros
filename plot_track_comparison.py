import os
import logging
from stringprep import c22_specials
from ROOT import TH1D, TH2D, TFile, TTree, TColor, TCanvas, TLegend, TLine, TLatex, TMath, TEfficiency, TF1
from ROOT import kBlack, kBlue, kRed, kGray, kGreen, kWhite
from ROOT import gStyle, gPad, gROOT
from ROOT import gROOT
from ROOT import TStyle
from optparse import OptionParser
import itertools
from math import fabs
from array import array

gROOT.SetBatch(True)

# Options
parser = OptionParser()
parser.add_option("-i", "--inFile",   dest='inFile',
                  default="histos_timing.root", help="Name of the ROOT histo file")
parser.add_option("-b", "--inFileBIB",   dest='inFileBIB',
                  default="histos_timing.root", help="Name of the ROOT histo file")
parser.add_option("-o", "--outFolder",   dest='outFolder',
                  default=".", help="Name of the output folder")
(options, args) = parser.parse_args()

# Init the logger for the script and various modules
fFile = TFile(options.inFile, "READ")
fFileBIB = TFile(options.inFileBIB, "READ")

gStyle.SetOptStat(0)
gStyle.SetPadTickY(1)
gStyle.SetPadTickX(1)

c2 = TCanvas("", "", 800, 680)
c2.SetTopMargin(0.1)
c2.SetRightMargin(0.05)
c2.SetBottomMargin(0.15)
c2.SetLeftMargin(0.15)

# Define features here
h_reco = fFile.Get('track_pT_central')
h_reco.Sumw2()
h_tot = fFile.Get('truth_pT_central')
h_tot.Sumw2()

eff_std = TEfficiency(h_reco, h_tot)
eff_std.SetLineColor(kRed)
eff_std.SetLineWidth(2)

h_recobib = fFileBIB.Get('track_pT_central')
h_recobib.Sumw2()
h_totbib = fFileBIB.Get('truth_pT_central')
h_totbib.Sumw2()

eff_bib = TEfficiency(h_recobib, h_totbib)
eff_bib.SetLineColor(kBlue)
eff_bib.SetLineWidth(2)

arrBins_pT = array('d', (0., 0.5, 1., 1.5, 2., 2.5, 3.,
                         3.5, 4., 5., 6., 7., 8., 10.))
# arrBins_pT = array('d', (0., 0.5, 1., 1.5, 2., 2.5, 3.,
#                         3.5, 4., 5., 6., 7., 8., 10., 20., 30., 50., 75., 100., 250., 500.))
h_frame = TH1D('framec2', 'framec2', len(arrBins_pT)-1, arrBins_pT)

h_frame.SetTitle("")
h_frame.GetYaxis().SetTitle("Track reconstruction efficiency")
h_frame.GetYaxis().SetTitleOffset(1.2)
h_frame.GetXaxis().SetTitleOffset(1.2)
h_frame.GetXaxis().SetTitleSize(0.04)
h_frame.GetYaxis().SetTitleSize(0.04)
h_frame.GetXaxis().SetTitle("Truth particle p_{T} [GeV]")
h_frame.SetMinimum(0.)
h_frame.SetMaximum(1.05)

h_frame.Draw()
eff_std.Draw("E0SAME")
eff_bib.Draw("E0SAME")

gPad.RedrawAxis()

leg = TLegend(.2, .2, .5, .35)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.04)
leg.AddEntry(eff_std, "w/o BIB+IPP", "L")
leg.AddEntry(eff_bib, "with BIB+IPP", "L")
leg.Draw()

t1 = TLatex()
t1.SetTextFont(42)
t1.SetTextColor(1)
t1.SetTextSize(0.04)
t1.SetTextAlign(12)
t1.SetNDC()
t1.DrawLatex(0.53, 0.7, '#bf{#it{Muon Collider}}')

t1_2 = TLatex()
t1_2.SetTextFont(42)
t1_2.SetTextColor(1)
t1_2.SetTextSize(0.04)
t1_2.SetTextAlign(12)
t1_2.SetNDC()
t1_2.DrawLatex(0.53, 0.64, 'Simulation, with BIB+IPP')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.04)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.53, 0.58, 'EU24 Lattice, #sqrt{s} = 10 TeV')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.04)
t3.SetTextAlign(12)
t3.SetNDC()
t3.DrawLatex(0.63, 0.94, '#it{MAIA} Detector Concept')

t2_3 = TLatex()
t2_3.SetTextFont(42)
t2_3.SetTextColor(1)
t2_3.SetTextSize(0.04)
t2_3.SetTextAlign(12)
t2_3.SetNDC()
t2_3.DrawLatex(.53, 0.31, 'Muon particle gun')
t2_3.DrawLatex(.53, 0.23, 'Uniform in p_{T} and #theta')

c2.SaveAs(options.outFolder+"/Track_Efficiency_vs_pT.pdf")

c3 = TCanvas("", "", 800, 680)
c3.SetTopMargin(0.1)
c3.SetRightMargin(0.05)
c3.SetBottomMargin(0.15)
c3.SetLeftMargin(0.15)

# Define features here
h_reco = fFile.Get('track_theta')
h_reco.Sumw2()
h_tot = fFile.Get('truth_theta')
h_tot.Sumw2()

eff_std = TEfficiency(h_reco, h_tot)
eff_std.SetLineColor(kRed)
eff_std.SetLineWidth(2)

h_recobib = fFileBIB.Get('track_theta')
h_recobib.Sumw2()
h_totbib = fFileBIB.Get('truth_theta')
h_totbib.Sumw2()

eff_bib = TEfficiency(h_recobib, h_totbib)
eff_bib.SetLineColor(kBlue)
eff_bib.SetLineWidth(2)


arrBins_theta = array('d', (0., 10.*TMath.Pi()/180., 30.*TMath.Pi()/180., 40.*TMath.Pi()/180., 50.*TMath.Pi()/180., 60.*TMath.Pi()/180., 70.*TMath.Pi()/180.,
                            90.*TMath.Pi()/180., 110.*TMath.Pi()/180., 120.*TMath.Pi()/180., 130.*TMath.Pi()/180., 140.*TMath.Pi()/180., 150.*TMath.Pi()/180., 170.*TMath.Pi()/180., TMath.Pi()))
h_frame = TH1D('framec3', 'framec3', len(arrBins_theta)-1, arrBins_theta)

h_frame.SetLineColor(kBlack)
h_frame.SetLineWidth(2)
h_frame.SetTitle("")
h_frame.GetYaxis().SetTitle("Track reconstruction efficiency")
h_frame.GetXaxis().SetTitleSize(0.04)
h_frame.GetYaxis().SetTitleSize(0.04)
h_frame.GetYaxis().SetTitleOffset(1.2)
h_frame.GetXaxis().SetTitleOffset(1.2)
# h_frame.GetXaxis().SetRangeUser(-0.24, 0.5)
h_frame.GetXaxis().SetTitle("Truth particle #theta [rad]")
h_frame.SetMinimum(0.8)
h_frame.SetMaximum(1.03)

h_frame.Draw()
eff_std.Draw("E0SAME")
eff_bib.Draw("E0SAME")

gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

leg = TLegend(.65, .2, .97, .36)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.04)
leg.AddEntry(eff_std, "w/o BIB+IPP", "L")
leg.AddEntry(eff_bib, "with BIB+IPP", "L")
leg.Draw()

t1 = TLatex()
t1.SetTextFont(42)
t1.SetTextColor(1)
t1.SetTextSize(0.04)
t1.SetTextAlign(12)
t1.SetNDC()
t1.DrawLatex(0.2, 0.53, '#bf{#it{Muon Collider}}')

t1_2 = TLatex()
t1_2.SetTextFont(42)
t1_2.SetTextColor(1)
t1_2.SetTextSize(0.04)
t1_2.SetTextAlign(12)
t1_2.SetNDC()
t1_2.DrawLatex(0.2, 0.47, 'Simulation, with BIB+IPP')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.04)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.2, 0.41, 'EU24 Lattice, #sqrt{s} = 10 TeV')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.04)
t3.SetTextAlign(12)
t3.SetNDC()
t3.DrawLatex(0.63, 0.94, '#it{MAIA} Detector Concept')

t2_3 = TLatex()
t2_3.SetTextFont(42)
t2_3.SetTextColor(1)
t2_3.SetTextSize(0.04)
t2_3.SetTextAlign(12)
t2_3.SetNDC()
t2_3.DrawLatex(.2, 0.31, 'Muon particle gun')
t2_3.DrawLatex(.2, 0.23, 'Uniform in p_{T} and #theta')

c3.SaveAs(options.outFolder+"/MAIA_Track_Efficiency_vs_theta.pdf")

c4 = TCanvas()
# Define features here
h_reco = fFile.Get('track_z0')
h_reco.Sumw2()
h_tot = fFile.Get('truth_z0')
h_tot.Sumw2()

eff_std = TEfficiency(h_reco, h_tot)
eff_std.SetLineColor(kBlue)
eff_std.SetLineWidth(2)

h_recobib = fFileBIB.Get('track_z0')
h_recobib.Sumw2()
h_totbib = fFileBIB.Get('truth_z0')
h_totbib.Sumw2()

eff_bib = TEfficiency(h_recobib, h_totbib)
eff_bib.SetLineColor(kRed)
eff_bib.SetLineWidth(2)

h_frame = TH1D('framec4', 'framec4', 100, -20., 20.)

h_frame.SetLineColor(kBlack)
h_frame.SetLineWidth(2)
h_frame.SetTitle("")
h_frame.GetYaxis().SetTitle("Track reconstruction efficiency")
h_frame.GetYaxis().SetTitleOffset(1.2)
h_frame.GetXaxis().SetTitleOffset(1.2)
# h_frame.GetXaxis().SetRangeUser(-0.24, 0.5)
h_frame.GetXaxis().SetTitle("Truth particle z [mm]")
h_frame.SetMinimum(0.0)
h_frame.SetMaximum(1.05)

h_frame.Draw()

eff_std.Draw("E0SAME")
eff_std.Draw("E0SAME")
h_tot.SetLineColor(kGray)
print(h_tot.Integral(), h_tot.GetMaximum())
h_tot.Scale(h_tot.GetMaximum()/h_tot.Integral())
h_tot.Draw("HISTSAME")
h_reco.SetLineColor(kGray+2)
h_reco.Scale(1./1100)
h_reco.Draw("HISTSAME")

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

t2_3 = TLatex()
t2_3.SetTextFont(42)
t2_3.SetTextColor(1)
t2_3.SetTextSize(0.035)
t2_3.SetTextAlign(12)
t2_3.SetNDC()
t2_3.DrawLatex(.17, 0.26, 'Muon particle gun')
t2_3.DrawLatex(.17, 0.2, 'Uniform in p_{T} (0.5, 50) GeV and #theta')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
t3.DrawLatex(0.15, 0.94, 'No background hit overlay')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

'''
leg = TLegend(.12, .8, .5, .92)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.AddEntry(eff_std, "Standard tracks", "L")
leg.Draw()
'''
c4.SaveAs(options.outFolder+"/Track_Efficiency_vs_z.pdf")


h_resolution = TH2D('resolution_pT', 'resolution_pT', len(
    arrBins_pT)-1, arrBins_pT, 100, -0.005, 0.005)
h_resolution_theta = TH2D('resolution_theta', 'resolution_theta', len(
    arrBins_theta)-1, arrBins_theta, 100, -0.005, 0.005)

tree = fFile.Get("tracks_tree")
for entry in tree:
    if entry.pT_truth > 0:
        h_resolution.Fill(entry.pT_truth, (entry.pT_truth -
                          entry.pT)/(entry.pT_truth*entry.pT_truth))
        h_resolution_theta.Fill(entry.theta, (entry.pT_truth -
                                              entry.pT)/(entry.pT_truth*entry.pT_truth))

h_reso_pT = TH1D('reso_pT', 'reso_pT',
                 len(arrBins_pT)-1, arrBins_pT)
for bin in range(0, len(arrBins_pT)-1):
    h_my_proj = h_resolution.ProjectionY("_py", bin, bin+1)
    gaussFit = TF1("gaussfit", "gaus")
    h_my_proj.Fit(gaussFit, "E")
    sigma = gaussFit.GetParameter(2)
    sigma_err = gaussFit.GetParError(2)
    h_reso_pT.SetBinContent(bin+1, sigma)
    h_reso_pT.SetBinError(bin+1, sigma_err)

h_reso_theta = TH1D('reso_theta', 'reso_theta',
                    len(arrBins_theta)-1, arrBins_theta)
for bin in range(0, len(arrBins_theta)-1):
    h_my_proj = h_resolution_theta.ProjectionY("_py", bin, bin+1)
    gaussFit = TF1("gaussfit", "gaus")
    h_my_proj.Fit(gaussFit, "E")
    sigma = gaussFit.GetParameter(2)
    sigma_err = gaussFit.GetParError(2)
    h_reso_theta.SetBinContent(bin+1, sigma)
    h_reso_theta.SetBinError(bin+1, sigma_err)

    if bin == 5:
        cdebug = TCanvas("", "", 800, 600)
        # h_resolutionAlt.Draw("COLZ")
        h_my_proj.Draw()
        cdebug.SaveAs("debug.pdf")

c2 = TCanvas("", "", 800, 600)
h_reso_pT.SetTitle(" ")
h_reso_pT.SetLineColor(kBlack)
h_reso_pT.SetLineWidth(2)
# h_reso_pT.SetMaximum(0.035)
# h_reso_pT.SetMinimum(0.015)
h_reso_pT.GetYaxis().SetTitle(
    "Track p_{T} resolution #sigma(#Delta p_{T} / p_{T}^{2})")
h_reso_pT.GetYaxis().SetTitleOffset(1.5)
h_reso_pT.GetXaxis().SetTitleOffset(1.2)
# h_reso_pT.GetXaxis().SetRangeUser(0., 100.)
h_reso_pT.GetXaxis().SetTitle("Track p_{T} [GeV]")
h_reso_pT.Draw("E0")

t3.DrawLatex(0.15, 0.94, 'Background hits overlay in [-0.36 0.48] ns range')
t4.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

c2.SaveAs("reso_vs_pT.pdf")


c2_2 = TCanvas("", "", 800, 600)
h_reso_theta.SetTitle(" ")
h_reso_theta.SetLineColor(kBlack)
h_reso_theta.SetLineWidth(2)
# h_reso_theta.SetMaximum(0.035)
# h_reso_theta.SetMinimum(0.015)
h_reso_theta.GetYaxis().SetTitle(
    "Track p_{T} resolution #sigma(#Delta p_{T} / p_{T}^{2})")
h_reso_theta.GetYaxis().SetTitleOffset(1.5)
h_reso_theta.GetXaxis().SetTitleOffset(1.2)
# h_reso_theta.GetXaxis().SetRangeUser(0., 100.)
h_reso_theta.GetXaxis().SetTitle("Track #theta [rad]")
h_reso_theta.Draw("E0")

#t3.DrawLatex(0.1, 0.94, 'No background hit overlay')
t3.DrawLatex(0.1, 0.94, 'BIB+IPP hits overlay')
t4.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

c2_2.SaveAs("reso_vs_theta.pdf")

'''
gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.15)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

c5 = TCanvas("", "", 800, 600)

# Define features here
h_reco = fFile.Get('track_theta_pT')
h_tot = fFile.Get('truth_theta_pT')
h_reco.Divide(h_tot)

h_reco.SetTitle("")
h_reco.GetZaxis().SetTitle("Seeding efficiency")
h_reco.GetZaxis().SetTitleOffset(1.2)
h_reco.GetYaxis().SetTitleOffset(1.2)
h_reco.GetYaxis().SetRangeUser(0.,5.)
h_reco.GetXaxis().SetTitleOffset(1.2)
h_reco.GetYaxis().SetTitle("Truth particle p_{T} [GeV]")
h_reco.GetXaxis().SetTitle("Truth particle #theta [rad]")
h_reco.SetMinimum(0.0)
h_reco.SetMaximum(1.0)

h_reco.Draw("COLZ")

t2_3 = TLatex()
t2_3.SetTextFont(42)
t2_3.SetTextColor(1)
t2_3.SetTextSize(0.035)
t2_3.SetTextAlign(12)
t2_3.SetNDC()
t2_3.DrawLatex(.17, 0.2, 'Muon particle gun, uniform in p_{T} (0.5, 50) GeV and #theta')

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()
t3.DrawLatex(0.15, 0.94, 'No background hit overlay')

t4 = TLatex()
t4.SetTextFont(42)
t4.SetTextColor(1)
t4.SetTextSize(0.035)
t4.SetTextAlign(12)
t4.SetNDC()
t4.DrawLatex(0.72, 0.94, '#sqrt{s} = 10 TeV')

c5.SaveAs(options.outFolder+"/Track_Efficiency_vs_theta_pT.pdf")


c5a = TCanvas("", "", 800, 600)

# Define features here
h_match = fFile.Get('n_matched_seed')
h_all = fFile.Get('n_seed')

h_all.SetTitle("")
h_all.GetZaxis().SetTitleOffset(1.2)
h_all.GetYaxis().SetTitleOffset(1.2)
h_all.GetXaxis().SetTitleOffset(1.2)
h_all.GetXaxis().SetTitle("Track seeds")
h_match.SetLineWidth(2)
h_match.SetLineColor(kBlue)

h_all.SetLineWidth(2)
h_all.SetLineColor(kRed)
h_all.GetXaxis().SetRangeUser(0., 10.)
h_all.SetMaximum(1.1*h_match.GetMaximum())

h_all.Draw("HIST")
h_match.Draw("HISTSAME")

leg = TLegend(.52, .7, .85, .85)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.AddEntry(h_all, "All Seeds", "L")
leg.AddEntry(h_match, "Matched Seeds", "L")
leg.Draw()

c5a.SaveAs(options.outFolder+"/Nseeds.pdf")

'''

fFile.Close()
