import os
import logging
from ROOT import TH1D, TH2D, TFile, TTree, TColor, TCanvas, TLegend, TLatex, TLine, TMath, TGraphErrors, TF1, TProfile
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
                  default="histos_photon.root", help="Name of the ROOT file")
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

arrBins_theta = array('d', (0., 30.*TMath.Pi()/180., 40.*TMath.Pi()/180., 50.*TMath.Pi()/180., 60.*TMath.Pi()/180., 70.*TMath.Pi()/180.,
                            90.*TMath.Pi()/180., 110.*TMath.Pi()/180., 120.*TMath.Pi()/180., 130.*TMath.Pi()/180., 140.*TMath.Pi()/180., 150.*TMath.Pi()/180., TMath.Pi()))
arrBins_E = array('d', (0., 5., 10., 15., 20., 25., 50.,
                  100., 250., 500., 1000., 1500., 2500., 5000.))
arrBins_Eres = array('d', (0., 20., 30., 40., 50., 60., 70., 80., 100., 120., 140., 160., 180., 200., 250., 300., 350., 400.,
                     500., 600., 700., 800., 900., 1000.))

arrBins_response = array('d', (0., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15., 17., 20.,
                               25., 30., 35., 40., 45., 50., 55., 60., 65., 70., 75., 80., 85., 90, 95., 100.,
                               110., 120., 130., 140., 150., 200., 250., 300., 350., 400., 450., 500., 550.,
                               600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 2000.,
                               2500., 3000., 4000., 5000.))

h_response = TH2D('photon_response', 'photon_response',
                  1000, 0, 500, 1000, 0, 500)
h_response_profile = TProfile('photon_response_profile', 'photon_response_profile',
                              len(arrBins_response)-1, arrBins_response, 0, 5000)
h_deltaresponse = TH2D('delta_response', 'delta_response',
                       100, 0, 500, 100, -1., 1.)

tree = fFile.Get("photon_tree")
for entry in tree:
    h_response.Fill(entry.E_truth, entry.E_alt)
    h_response_profile.Fill(entry.E_truth, entry.E_alt)
    h_deltaresponse.Fill(
        entry.E_truth, (entry.E_alt - entry.E_truth)/entry.E_truth)

h_reso_theta = TH1D('reso_theta', 'reso_theta',
                    len(arrBins_theta)-1, arrBins_theta)
h_reso_theta_20_50 = TH1D('reso_theta_20_50', 'reso_theta_20_50',
                          len(arrBins_theta)-1, arrBins_theta)
h_reso_theta_50_250 = TH1D('reso_theta_50_250', 'reso_theta_50_250',
                           len(arrBins_theta)-1, arrBins_theta)
h_reso_theta_250_up = TH1D('reso_theta_250_up', 'reso_theta_250_up',
                           len(arrBins_theta)-1, arrBins_theta)
h1_reso_E = TH1D('reso_E', 'reso_E',
                 len(arrBins_Eres)-1, arrBins_Eres)

e_arr = array('d')
sigma_arr = array('d')
e_err_arr = array('d')
sigma_err_arr = array('d')

cx = TCanvas("", "", 800, 600)
gStyle.SetOptStat(1)

for bin in range(0, len(arrBins_Eres)-1):
    minE = arrBins_Eres[bin]
    maxE = arrBins_Eres[bin+1]

    proj_name = "ph_E"+str(arrBins_Eres[bin])+"_py"
    h_my_proj = TH1D(proj_name, proj_name, 250, -2.5, 2.5)

    dR_match = sqrt((entry.phi_alt - entry.phi_truth)*(entry.phi_alt - entry.phi_truth)+(entry.theta_alt - entry.theta_truth)*(entry.theta_alt - entry.theta_truth))

    for entry in tree:
        if entry.E > 0:
            if dR_match < 0.1:
                if entry.hfrac_alt<0.1:
                    if (entry.E_truth > minE) and (entry.E_truth < maxE):
                        if (entry.E_alt - entry.E_truth)/entry.E_truth > -0.5:
                            h_my_proj.Fill((entry.E_alt - entry.E_truth)/entry.E_truth)

    if minE < 160.:
        gaussFit = TF1("gaussfit", "gaus", h_my_proj.GetMean()-2.*h_my_proj.GetRMS(), h_my_proj.GetMean()+2.*h_my_proj.GetRMS())
        gaussFit.SetParameter(1, h_my_proj.GetMean())
        gaussFit.SetParameter(2, h_my_proj.GetRMS())
        h_my_proj.Fit(gaussFit, "E")
        h_my_proj.Draw("HIST")
        gaussFit.Draw("LSAME")
        cx.SaveAs("slices_ph/"+proj_name+".pdf")
        sigma = gaussFit.GetParameter(2)
        sigma_err = gaussFit.GetParError(2)
        if bin > 0:
            e_arr.append(h1_reso_E.GetBinCenter(bin+1))
            e_err_arr.append(0.)
            sigma_arr.append(sigma)
            sigma_err_arr.append(sigma_err)
    else:
        gaussFit = TF1("gaussfit", "gaus", -0.15, 0.15)
        gaussFit.SetParameter(1, h_my_proj.GetMean())
        gaussFit.SetParameter(2, h_my_proj.GetRMS())
        h_my_proj.Fit(gaussFit, "E")
        h_my_proj.Draw("HIST")
        gaussFit.Draw("LSAME")
        cx.SaveAs("slices_ph/"+proj_name+".pdf")
        sigma = gaussFit.GetParameter(2)
        sigma_err = gaussFit.GetParError(2)
        if bin > 0:
            e_arr.append(h1_reso_E.GetBinCenter(bin+1))
            e_err_arr.append(0.)
            sigma_arr.append(sigma)
            sigma_err_arr.append(sigma_err)


h_reso_E = TGraphErrors(len(e_arr), e_arr, sigma_arr, e_err_arr, sigma_err_arr)

c2_2 = TCanvas("", "", 800, 600)

h_reso_E.SetTitle(" ")
# h_reso_E.SetMaximum(1.2)
# h_reso_E.SetMinimum(0.005)
h_reso_E.GetYaxis().SetTitle("Photon #sigma_{E}/E")
h_reso_E.GetYaxis().SetTitleOffset(1.4)
h_reso_E.GetXaxis().SetTitleOffset(1.2)
h_reso_E.GetXaxis().SetTitle("True photon energy [GeV]")

resoFit = TF1(
    "resofit", "sqrt([0]*[0]/x+[1]*[1]/(x*x)+[2]*[2])", 20., 1000., 3)
resoFit.SetParName(0, "Stochastic")
resoFit.SetParName(1, "Noise")
resoFit.SetParName(2, "Constant")
resoFit.SetParameter(0, 0.5)
resoFit.SetParameter(1, 0.)
resoFit.SetParameter(2, 0.)
h_reso_E.Fit(resoFit, "R")

h_reso_E.SetLineColor(kBlack)
h_reso_E.SetLineWidth(2)
h_reso_E.Draw("AP")

resoFit.Draw("LSAME")
h_reso_E.Draw("PSAME")

h_reso_E.GetXaxis().SetRangeUser(10., 1000.)
h_reso_E.GetYaxis().SetRangeUser(0.01, 0.5)

c2_2.Update()
c2_2.SetLogy()

leg = TLegend(.35, 0.8, .65, 0.85)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(h_reso_E, "Variable cell threshold and BIB subtraction", "L")
leg.Draw()

t3 = TLatex()
t3.SetTextFont(42)
t3.SetTextColor(1)
t3.SetTextSize(0.035)
t3.SetTextAlign(12)
t3.SetNDC()

t3.DrawLatex(0.15, 0.94, 'Background hits overlay in [-0.5, 15] ns range')
t3.DrawLatex(0.82, 0.94, '#sqrt{s} = 10 TeV')

t3.DrawLatex(0.6, 0.72, 'Stochastic = %.3f' % resoFit.GetParameter(0))
t3.DrawLatex(0.6, 0.66, 'Noise = %.3f' % resoFit.GetParameter(1))
t3.DrawLatex(0.6, 0.6, 'Constant = %.3f' % resoFit.GetParameter(2))

c2_2.SaveAs("reso_vs_E.pdf")

fFile.Close()
