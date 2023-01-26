import sys
from globalmod import *

### define energy here:
Energy=20
#####################

myinput="interactive"
if (len(sys.argv) ==2):
   myinput = sys.argv[1]


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
print ('Use as: script.py -b 0 (or 1,2)')

############# Configs ##############
nameX="R=N_{Ch} / N_{Sc}"
nameY="Events / total"


Xmin=0.001 
Xmax=1.1
Ymin=0. 
Ymax=0.99 

import sys
epsfig="figs/"+sys.argv[0].replace(".py",".eps")


gROOT.SetStyle("Plain");
xwin=600
ywin=800
c1=TCanvas("c","Mass",10,10,xwin,ywin);
c1.SetFrameBorderMode(0);
c1.Divide(2,4);
#c1.Divide(2,4,0.02,0.02);
gPad.SetLeftMargin(0.2);
c1.SetLeftMargin(0.2);

ps1 = TPostScript( epsfig,113)
c1.SetTickx()
c1.SetTicky()
c1.SetTitle("")
c1.SetLineWidth(3)
c1.SetFillColor(0)


particles=["e-","gamma","pi0","mu-","pi-","neutron","proton","kaon-"] 

e=Energy;

legends=[]

for i in range(8):
  leg2=TLegend(0.15, 0.8, 0.4, 0.92);
  leg2.SetBorderSize(0);
  leg2.SetTextFont(62);
  leg2.SetFillColor(10);
  leg2.SetTextSize(0.1);
  legends.append(leg2)


for i in range(8):
  c1.cd(i+1);

  gPad.SetLeftMargin(0.135)
  print("Draw pad=",i)
  gPad.SetRightMargin(0.01);
  if i>0:
          if (i%2 !=0): 
                     gPad.SetLeftMargin(0.001);
                     gPad.SetRightMargin(0.10);

  gPad.SetBottomMargin(0.005);
  gPad.SetTopMargin(0.005);

  if (i>5): gPad.SetBottomMargin(0.18);
  if (i<2): gPad.SetTopMargin(0.05);

  h=gPad.DrawFrame(Xmin,Ymin,Xmax,Ymax);
  h.Draw()
  ax=h.GetXaxis();
  ax.SetTitle( nameX );
  ay=h.GetYaxis();
  ay.SetTitle( nameY );

  ax.SetLabelSize(0.07)
  ax.SetTitleSize(0.09)
  ax.SetTitleOffset(1.0)
  ay.SetTitleOffset(0.9)

  ay.SetLabelSize(0.07)
  ay.SetTitleSize(0.08)
  gPad.SetTickx()
  gPad.SetTicky()

  if (i==0 or i==2 or i==4 or i==6):
    ay.Draw("same")
    #ax.Draw("same")

  if (i==1 or i==3 or i==5 or i==7):
    ay.SetTitleSize(0.0)
    ay.SetLabelSize(0.0)
  if (i<6):
    ax.SetTitleSize(0.0)
    ax.SetLabelSize(0.0)
    
  part=particles[i]

  fname="histos/hist_"+part+"_"+str(e)+"gev.root"
  xfile0=TFile( fname )
  hh0=xfile0.Get("cherenkDIVscintil")
  hh0.SetDirectory(0)
  xfile0.Close()

  hh0.Scale(1.0/hh0.Integral())
  hh0.SetMarkerColor( 0 )
  hh0.SetMarkerStyle(0)
  hh0.SetLineColor( 1 )
  hh0.SetLineWidth(1)
  hh0.SetFillColor(7)
  hh0.Draw("same histo")
  mean0='%.2f'%( hh0.GetMean()  )

  leg2=legends[i]

  pp=part
  if (pp=="muon-"): pp="#mu^{-}"
  if (pp=="gamma"): pp="#gamma"
  if (pp=="kaon-"): pp="K^{-}"
  if (pp=="proton"): pp="p"
  if (pp=="neutron"): pp="n"
  if (pp=="pi0"): pp="#pi^{0}"
  if (pp=="pi-"): pp="#pi^{-}"
 
  #leg2.AddEntry(hh0,"<R("+pp+")>= "+str(mean0),"fl")
  #leg2.Draw("same");


  myTextUser(0.06,0.88,1,0.1,str(e)+" GeV")
  myTextUser(0.32,0.88,1,0.1,"<R("+pp+")>= "+str(mean0))

gPad.RedrawAxis()
c1.Update()


if (myinput != "-b"):
              if (input("Press any key to exit") != "-9999"):
                         c1.Close(); sys.exit(1);

