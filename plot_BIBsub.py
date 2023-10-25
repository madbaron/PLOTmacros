import os
import logging
from ROOT import TH1D, TH2D, TGraph2D, TFile, TTree, TColor, TCanvas, TLegend, TLatex, TLine, TMath, TEfficiency, TF1
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


N_sigma = 5
early_ev_limit = 1000000000  # use only for debug
isECAL = 0

gStyle.SetPaintTextFormat("1.3f")

# Options
parser = OptionParser()
parser.add_option("-i", "--inFile",   dest='inFile',
                  default="../MuCData/ntup_BIBsub.root", help="Name of the ROOT file")
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

arrBins_theta_sym = array('d', (0., 30.*TMath.Pi()/180., 40.*TMath.Pi()/180., 45.*TMath.Pi()/180., 50. *
                          TMath.Pi()/180., 55.*TMath.Pi()/180., 60.*TMath.Pi()/180., 70.*TMath.Pi()/180., 90.*TMath.Pi()/180.))

max_layer = 0
if isECAL:
    arrBins_layer = array('d', (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                10, 12, 14, 16, 18, 20, 22, 26, 30, 35, 40, 50))
    max_layer = 50
else:
    arrBins_layer = array('d', (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                10, 12, 14, 16, 18, 20, 22, 26, 30, 35, 40, 50, 70, 100))
    max_layer = 100

layer_map = []
for layer in range(0, max_layer):
    name = 'hit_E_vs_theta_layer' + str(layer)
    histo = TH2D(name, name, len(arrBins_theta)-1, arrBins_theta, 100, 0, 0.1)
    layer_map.append(histo)


layer_map_sym = []
if isECAL:
    layer_group = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   12, 14, 16, 18, 20, 22, 26, 30, 35, 40, 50]
    layer_denom = [1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 2, 2, 2, 2, 2, 2, 4, 4, 5, 5, 10]
else:
    layer_group = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   12, 14, 16, 18, 20, 22, 26, 30, 35, 40, 50, 70, 100]
    layer_denom = [1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 2, 2, 2, 2, 2, 2, 4, 4, 5, 5, 10, 20, 30]

for layer in layer_group:
    name_sym = 'hit_E_vs_theta_layer_sym' + str(layer)
    histo_sym = TH2D(name_sym, name_sym, len(
        arrBins_theta_sym)-1, arrBins_theta_sym, 100, 0, 0.1)
    layer_map_sym.append(histo_sym)

tree = fFile.Get("hit_tree")

N_total_hits = 0
for ientry, entry in enumerate(tree):

    if ientry >= early_ev_limit:
        break

    if entry.isECAL == isECAL:
        layer_map[entry.layer].Fill(entry.theta, entry.E)
        N_total_hits = N_total_hits + 1

        # find bin
        the_bin = 0
        for ilow, low in enumerate(layer_group):
            if entry.layer >= low:
                the_bin = ilow

        # Fill sym histo
        if entry.theta > TMath.Pi()/2:
            flipped_theta = TMath.Pi()-entry.theta
            layer_map_sym[the_bin].Fill(
                flipped_theta, entry.E, 1./layer_denom[the_bin])
        else:
            layer_map_sym[the_bin].Fill(
                entry.theta, entry.E, 1./layer_denom[the_bin])

print("Total hits: ", N_total_hits)

x_graph = array('d', [0])
y_graph = array('d', [0])
z_graph_mean = array('d', [0])
z_graph_max = array('d', [0])
z_graph_stddev = array('d', [0])

cx = TCanvas("", "", 800, 600)
gStyle.SetOptStat(1)

threshold_map = []
for layer in range(0, max_layer):
    threshold_map_theta = []
    for bin in range(len(arrBins_theta)-1):
        proj_name = str(layer)+"_bin"+str(bin)+"_py"
        h_my_proj = layer_map[layer].ProjectionY(proj_name, bin, bin+1)
        h_my_proj.Draw("HIST")
        cx.SaveAs("slices/"+proj_name+".pdf")
        threshold_map_theta.append(
            h_my_proj.GetMean() + N_sigma*h_my_proj.GetStdDev())

        x_center = (arrBins_theta[bin+1]+arrBins_theta[bin])/2
        x_graph.append(x_center)
        y_graph.append(layer)

        binmax = h_my_proj.GetMaximumBin()
        x_max = h_my_proj.GetXaxis().GetBinCenter(binmax)

        z_graph_mean.append(h_my_proj.GetMean())
        z_graph_max.append(x_max)
        z_graph_stddev.append(h_my_proj.GetStdDev())

    threshold_map.append(threshold_map_theta)

x_graph_sym = array('d', [0])
y_graph_sym = array('d', [0])
z_graph_sym_mean = array('d', [0])
z_graph_sym_max = array('d', [0])
z_graph_sym_stddev = array('d', [0])

for layer in range(len(layer_group)):
    for bin in range(len(arrBins_theta_sym)-1):
        h_my_proj = layer_map_sym[layer].ProjectionY("_py", bin, bin+1)

        x_center = (arrBins_theta_sym[bin+1]+arrBins_theta_sym[bin])/2
        x_graph_sym.append(x_center)
        y_graph_sym.append(layer_group[layer])
        binmax = h_my_proj.GetMaximumBin()
        x_max = h_my_proj.GetXaxis().GetBinCenter(binmax)

        z_graph_sym_mean.append(h_my_proj.GetMean())
        z_graph_sym_max.append(x_max)
        z_graph_sym_stddev.append(h_my_proj.GetStdDev())

# print(x_graph)
# print(y_graph)
# print(z_graph)

N_passed_hits = 0
for ientry, entry in enumerate(tree):

    if ientry >= early_ev_limit:
        break

    if entry.isECAL == isECAL:
        binx = layer_map[entry.layer].GetXaxis().FindBin(entry.theta)
        if entry.E > threshold_map[entry.layer][binx-1]:
            N_passed_hits = N_passed_hits + 1

print("Passed hits: ", N_passed_hits)
print("Efficiency: ", N_passed_hits/N_total_hits)

# Plotting the thresholds

gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.15)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

histo_mode = TH2D("2dmode", "2dmode", len(
    arrBins_theta)-1, arrBins_theta, 50, 0, 50)
histo_mean = TH2D("2dmean", "2dmean", len(
    arrBins_theta)-1, arrBins_theta, 50, 0, 50)
histo_th_mode = TH2D("th_2dmode", "th_2dmode", len(
    arrBins_theta)-1, arrBins_theta, 50, 0, 50)
histo_th_mean = TH2D("th_2dmean", "th_2dmean", len(
    arrBins_theta)-1, arrBins_theta, 50, 0, 50)

for i in range(len(x_graph)):
    histo_mode.Fill(x_graph[i], y_graph[i], z_graph_max[i])
    histo_mean.Fill(x_graph[i], y_graph[i], z_graph_mean[i])
    histo_th_mode.Fill(x_graph[i], y_graph[i],
                       z_graph_max[i]+N_sigma*z_graph_stddev[i])
    histo_th_mean.Fill(x_graph[i], y_graph[i],
                       z_graph_mean[i]+N_sigma*z_graph_stddev[i])

c1a = TCanvas("", "", 800, 600)
histo_mean.Draw("COLZTEXT")
histo_mean.SetMinimum(0)
c1a.SaveAs("mean_vs_theta_layer.pdf")

c2a = TCanvas("", "", 800, 600)
histo_mode.Draw("COLZTEXT")
histo_mode.SetMinimum(0)
c2a.SaveAs("mode_vs_theta_layer.pdf")

c1 = TCanvas("", "", 800, 600)
histo_th_mean.Draw("COLZTEXT")
histo_th_mean.SetMinimum(0)
c1.SaveAs("mean_threshold_vs_theta_layer.pdf")

c2 = TCanvas("", "", 800, 600)
histo_th_mode.Draw("COLZTEXT")
histo_th_mode.SetMinimum(0)
c2.SaveAs("mode_threshold_vs_theta_layer.pdf")

histo_mode_sym = TH2D("2dmode_sym", "2dmode_sym", len(
    arrBins_theta_sym)-1, arrBins_theta_sym, len(arrBins_layer)-1, arrBins_layer)
histo_mean_sym = TH2D("2dmean_sym", "2dmean_sym", len(
    arrBins_theta_sym)-1, arrBins_theta_sym, len(arrBins_layer)-1, arrBins_layer)
histo_th_mode_sym = TH2D("th_2dmode_sym", "th_2dmode_sym", len(
    arrBins_theta_sym)-1, arrBins_theta_sym, len(arrBins_layer)-1, arrBins_layer)
histo_th_mean_sym = TH2D("th_2dmean_sym", "th_2dmean_sym", len(
    arrBins_theta_sym)-1, arrBins_theta_sym, len(arrBins_layer)-1, arrBins_layer)
histo_stddev_sym = TH2D("stddev_sym", "stddev_sym", len(
    arrBins_theta_sym)-1, arrBins_theta_sym, len(arrBins_layer)-1, arrBins_layer)

histo_th_mean_sym.SetDirectory(0)
histo_th_mode_sym.SetDirectory(0)
histo_stddev_sym.SetDirectory(0)


for i in range(len(x_graph_sym)):
    histo_mode_sym.Fill(x_graph_sym[i], y_graph_sym[i], z_graph_sym_max[i])
    histo_mean_sym.Fill(x_graph_sym[i], y_graph_sym[i], z_graph_sym_mean[i])
    histo_th_mode_sym.Fill(
        x_graph_sym[i], y_graph_sym[i], z_graph_sym_max[i]+N_sigma*z_graph_sym_stddev[i])
    histo_th_mean_sym.Fill(
        x_graph_sym[i], y_graph_sym[i], z_graph_sym_mean[i]+N_sigma*z_graph_sym_stddev[i])
    histo_stddev_sym.Fill(
        x_graph_sym[i], y_graph_sym[i], z_graph_sym_stddev[i])

c1_syma = TCanvas("", "", 800, 600)
histo_mean_sym.Draw("COLZTEXT")
histo_mean_sym.SetMinimum(0)
c1_syma.SaveAs("mean_vs_theta_layer_sym.pdf")

c2_syma = TCanvas("", "", 800, 600)
histo_mode_sym.Draw("COLZTEXT")
histo_mode_sym.SetMinimum(0)
c2_syma.SaveAs("mode_vs_theta_layer_sym.pdf")

c1_sym = TCanvas("", "", 800, 600)
histo_th_mean_sym.Draw("COLZTEXT")
histo_th_mean_sym.SetMinimum(0)
c1_sym.SaveAs("mean_threshold_vs_theta_layer_sym.pdf")

c2_sym = TCanvas("", "", 800, 600)
histo_th_mode_sym.Draw("COLZTEXT")
histo_th_mode_sym.SetMinimum(0)
c2_sym.SaveAs("mode_threshold_vs_theta_layer_sym.pdf")

c3_sym = TCanvas("", "", 800, 600)
histo_stddev_sym.Draw("COLZTEXT")
histo_stddev_sym.SetMinimum(0)
c3_sym.SaveAs("stddev_vs_theta_layer_sym.pdf")

fFile.Close()

# write out histograms
output_file = TFile("CAL_Thresholds.root", 'RECREATE')
histo_th_mean_sym.Write()
histo_th_mode_sym.Write()
histo_stddev_sym.Write()
output_file.Close()
