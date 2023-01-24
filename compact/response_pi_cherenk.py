import sys
from globalmod import *

myinput="interactive"
if (len(sys.argv) ==2):
   myinput = sys.argv[1]


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
print ('Use as: script.py -b 0 (or 1,2)')

############# Configs ##############
nameX="E [GeV]"
nameY="N_{#gamma}^{ Cherenkov}"

Xmin=0.3
Xmax=12.0
Ymin=0.
Ymax=2900000.

name="cherenk"

import sys
epsfig="figs/"+sys.argv[0].replace(".py",".eps")


gROOT.SetStyle("Plain");
xwin=600
ywin=600
c1=TCanvas("c","Mass",10,10,xwin,ywin);
c1.SetFrameBorderMode(0);
ps1 = TPostScript( epsfig,113)
c1.SetTickx()
c1.SetTicky()
c1.SetTitle("")
c1.SetLineWidth(3)
c1.SetBottomMargin(0.12)
c1.SetTopMargin(0.05)
c1.SetRightMargin(0.1)
c1.SetFillColor(0)
c1.SetLeftMargin(0.15)

# c1.SetLogy(1)
c1.SetLogx(0)

h=gPad.DrawFrame(Xmin,Ymin,Xmax,Ymax);
h.Draw()

ax=h.GetXaxis();
ax.SetTitle( nameX );
ay=h.GetYaxis();
ay.SetTitle( nameY );

ax.SetLabelSize(0.04)
ax.SetTitleSize(0.05)
ax.SetTitleOffset(1.0)
ay.SetTitleOffset(1.38)

ay.SetLabelSize(0.04)
ay.SetTitleSize(0.05)
gPad.SetTickx()
gPad.SetTicky()

ay.Draw("same")
ax.Draw("same")


energies=[0.5,1,5,10] 

ptmin=0.45 
ptmax=20
#s1="sqrt(([0]/sqrt(x))*([0]/sqrt(x))+([1]/x)*([1]/x)+[2]*[2])"
s1="([0]*(x))+[1]"

f1=TF1("f1",s1,ptmin,ptmax);
f1.SetLineStyle(1)
f1.SetLineWidth(2)
f1.SetLineColor(4)
f1.SetParameter(0,0.5)
f1.SetParameter(1,4.58662e-01)
#f1.FixParameter(1,0)
#f1.SetParameter(2,2.02282e-02)


i=0
elec=TGraphErrors()
for e in energies:
      fname="histos/hito_pi-_"+str(e)+"gev.root"
      xfile=TFile( fname )
      hh=xfile.Get(name)
      RMS=rms90(hh); 
      #RMS=hh.GetRMS()
      ERR=hh.GetRMSError()
      MEAN=hh.GetMean()  
      MEAN_ERR=hh.GetMeanError() 
      print(e," MEAN/E=",MEAN," RMS=",RMS," ERR=",ERR)
      elec.SetPoint(i,e,MEAN)
      elec.SetPointError(i,0, MEAN_ERR)
      i=i+1
elec.SetLineColor( 1 )
elec.SetMarkerColor( 2 )
elec.SetMarkerSize(1)
elec.SetMarkerStyle(21)
elec.SetLineWidth(3)
elec.SetLineStyle(1)
elec.Draw("][pe same")

for i in range(20):
     fitr=elec.Fit(f1,"SRE+","",ptmin,ptmax);
     print ("Status=",int(fitr), " is valid=",fitr.IsValid())
     if (fitr.IsValid()==True): break;
fitr.Print()
print ("Is valid=",fitr.IsValid())

par1 = f1.GetParameters()
a1='%.0f'%( par1[0] )
b1='%.0f'%( par1[1] )
#k1='%.2f'%( par1[2] )
#s1="#sqrt{"+a1+" ^{2} / E +"+b1+" ^{2}/E +"+k1+"^{2}}"
s1=a1+" x E+"+b1

leg2=TLegend(0.3, 0.68, 0.89, 0.94);
leg2.SetBorderSize(0);
leg2.SetTextFont(62);
leg2.SetFillColor(10);
leg2.SetTextSize(0.04);
leg2.AddEntry(elec,"Pions","pl")
leg2.AddEntry(f1,s1,"l")
leg2.Draw("same");


gPad.RedrawAxis()
c1.Update()


if (myinput != "-b"):
              if (input("Press any key to exit") != "-9999"):
                         c1.Close(); sys.exit(1);

