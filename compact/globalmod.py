from math import sqrt,acos,exp
from array import array
from ROOT import gROOT,gPad,gStyle,TCanvas,TSpline3,TFile,TLine,TLatex,TAxis,TLegend,TPostScript
from ROOT import TH2D,TArrow,TCut,TPad,TH1D,TF1,TObject,TPaveText,TGraph,TGraphErrors,TGraphAsymmErrors
from ROOT import TMath, TGraph2D,TTree,TMultiGraph,TBranch,gSystem,gDirectory
from ROOT import TPaveStats
import random

# par[1] - mean
# par[2] - sigma
class Gauss:
   def __call__( self, x, par ):
       out=par[0] * TMath.Gaus(x[0],par[1],par[2])
       return out;


# 90% RMS
# http://agenda.linearcollider.org/event/2703/contributions/8926/attachments/6867/11488/RMS90.pdf
# https://pdfs.semanticscholar.org/d98d/1dbf35236e45edbc4dc68aede5db6a82d294.pdf
# RMS90 is defined as the RMS falculated for a
# distribution in which 10% of the events in the tails
# are excluded from the RMS calculation
def rms90(h):
   axis = h.GetXaxis();
   nbins = axis.GetNbins();
   imean = axis.FindBin(h.GetMean());
   entries =0.9*h.GetEntries();
   w = h.GetBinContent(imean);
   x = h.GetBinCenter(imean);
   sumw = w;
   sumwx = w*x;
   sumwx2 = w*x*x;
   for i in range(1,nbins):
      if (i> 0):
         w = h.GetBinContent(imean-i);
         x = h.GetBinCenter(imean-i);
         sumw += w;
         sumwx += w*x;
         sumwx2 += w*x*x;
      if (i<= nbins):
         w = h.GetBinContent(imean+i);
         x = h.GetBinCenter(imean+i);
         sumw += w;
         sumwx += w*x;
         sumwx2 += w*x*x;
      if (sumw > entries): break;
   x = sumwx/sumw;
   rms2 = TMath.Abs(sumwx2/sumw -x*x)
   result = TMath.Sqrt(rms2)
   # print ("RMS of central 90% = ",result, " RMS total =",h.GetRMS());
   return 1.25*result


def myText(x,y,color=1,size=0.08,text=""):
  l=TLatex()
  l.SetTextSize(size);
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);

def myTextUser(x,y,color=1,size=0.08,text=""):
  l=TLatex()
  l.SetTextSize(size);
  #l.SetUser();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);

