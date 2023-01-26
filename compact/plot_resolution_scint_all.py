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
nameY="#sigma (N_{sc}) / N_{sc}"
name="scintil"
#####################################

Xmin=0.2 
Xmax=21.
Ymin=-0.001 
Ymax=1.01 

# energy points
energies=[0.5,1,5,10,20]


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


legends=[]
functions=[]
data=[]

# define functions
ptmin=0.45
ptmax=20
s1="sqrt(([0]/sqrt(x))*([0]/sqrt(x))+([1]/x)*([1]/x)+[2]*[2])"
#s1="([0]/sqrt(x))+[1]"
s1="([0]/x)+[1]"

for i in range(8):
  
  leg2=TLegend(0.20, 0.75, 0.4, 0.92);
  if (i==1 or i ==3 or i ==5 or i==7): leg2=TLegend(0.14, 0.75, 0.4, 0.92);
  leg2.SetBorderSize(0);
  leg2.SetTextFont(62);
  leg2.SetFillColor(10);
  leg2.SetTextSize(0.1);
  legends.append(leg2)

  f1=TF1("f1",s1,ptmin,ptmax);
  f1.SetLineStyle(1)
  f1.SetLineWidth(2)
  f1.SetLineColor(4)
  f1.SetParameter(0,0.08)
  f1.SetParameter(1,0.01)
  functions.append(f1)

  elec=TGraphErrors()
  elec.SetLineColor( 1 )
  elec.SetMarkerColor( 2 )
  elec.SetMarkerSize(1)
  elec.SetMarkerStyle(21)
  data.append(elec)

for i in range(8):
  c1.cd(i+1);

  #gPad.SetLogx(1)
  gPad.SetLeftMargin(0.18)
  print("Draw pad=",i)
  gPad.SetRightMargin(0.01);
  # second column
  if i>0:
          if (i%2 !=0): 
                     gPad.SetLeftMargin(0.11);
                     gPad.SetRightMargin(0.08);

  gPad.SetBottomMargin(0.06);
  gPad.SetTopMargin(0.005);

  if (i>5): gPad.SetBottomMargin(0.18);
  if (i<2): gPad.SetTopMargin(0.05);


  part=particles[i]

  elec=data[i] # take a graph

  MaxY=Ymax
  # fill this graph
  j=0
  for e in energies:
      fname="histos/hist_"+part+"_"+str(e)+"gev.root"
      xfile0=TFile( fname )
      hh=xfile0.Get(name)
      hh.SetDirectory(0)
      xfile0.Close()

      #if (part == "proton" or part=="neutron" or part=="kaon-"):
      #           if e==0.5:
      #                 continue

      # fit in each 
      MEAN=hh.GetMean()
      RMS=rms90(hh); # hh.GetRMS()
      ERR=hh.GetRMSError()

      # try fit 
      minfit=MEAN-3*RMS
      maxfit=MEAN+3*RMS
      print("Fin min and max",minfit,maxfit," center=",MEAN)

      binmax = hh.GetMaximumBin();
      yyy = 0.8*hh.GetBinContent(binmax);
      signal=TF1("signal",Gauss(),minfit,maxfit,3);
      signal.SetNpx(200); signal.SetLineColor(2); signal.SetLineStyle(1)
      signal.SetParameter(1, MEAN)
      signal.SetParameter(2, RMS)
      signal.SetParameter(0, yyy)
      signal.SetParLimits(2,0.00001,1000.0)

      fitr=hh.Fit(signal,"SR0E+","",minfit, maxfit);
      #print ("Status=",int(fitr), " is valid=",fitr.IsValid())
      status=fitr.IsValid()
      if (status):
            par = signal.GetParameters()
            err=signal.GetParErrors()
            RMS= par[2]
            ERR= err[2]

      #RMS=rms90(hh) # hh.GetRMS() # rms90(hh);
      #ERR=hh.GetRMSError()

      if (e==5): MaxY=(RMS/MEAN)*20  
      if (e<1.1 and part=="proton"): continue # Bragg peak -> avoid  
      print(part, e,"GeV  RMS=",RMS," MEAN=",MEAN," RMS/MEAN=",RMS/MEAN)
      elec.SetPoint(j,e,RMS/MEAN)
      elec.SetPointError(j,0.0,ERR/MEAN)
      j=j+1

  #if (i>5): MaxY=0.99
  Ymax=MaxY
  h=gPad.DrawFrame(Xmin,Ymin,Xmax,Ymax);
  h.Draw()
  ax=h.GetXaxis();
  ax.SetTitle( nameX );
  ay=h.GetYaxis();
  ay.SetTitle( nameY );

  ax.SetLabelSize(0.07)
  ax.SetTitleSize(0.09)
  ax.SetTitleOffset(1.0)
  ay.SetTitleOffset(1.15)

  ay.SetLabelSize(0.07)
  ay.SetTitleSize(0.08)
  gPad.SetTickx()
  gPad.SetTicky()

  #if (i==0 or i==2 or i==4 or i==6):
  #  ay.Draw("same")

  if (i==1 or i==3 or i==5 or i==7):
    ay.SetTitleSize(0.0)
    #ay.SetLabelSize(0.0)
  if (i<6):
    ax.SetTitleSize(0.0)
    #ax.SetLabelSize(0.0)

  ay.Draw("same")
   
  elec.Draw("][pe same")

  f1=functions[i] # take a function

  nn=0
  chi2min=10000
  parbest=[]
  for j in range(20):
     fitr=elec.Fit(f1,"SMR0")
     print "Status=",int(fitr), " is valid=",fitr.IsValid()
     if (fitr.IsValid()==True):
             chi2=f1.GetChisquare()/f1.GetNDF()
             if chi2<chi2min:
                    chi2min=chi2;
                    if nn>4:
                           break;
                    f1.SetParameter(0,random.randint(0,1))
                    f1.SetParameter(1,random.randint(0,1))
                    #f1.SetParameter(2,random.randint(0,50))
                    nn=nn+1
  fitr.Print()
  print ("Is valid=",fitr.IsValid())

  # do not show muons. They are MIP 
  #if (part != "mu-"): f1.Draw("same")

  par1 = f1.GetParameters()
  a1='%.3f'%( par1[0] )
  b1='(%.3f'%( par1[1] )+")"
  #k1='%.2f'%( par1[2] )
  #s1="#sqrt{"+a1+" ^{2} / E +"+b1+" ^{2}/E +"+k1+"^{2}}"
  #s1=a1+"/ \sqrt{E}+"+b1
  s1=a1+"/ E+"+b1 

  pp=part
  if (pp=="mu-"): pp="#mu^{-}"
  if (pp=="gamma"): pp="#gamma"
  if (pp=="kaon-"): pp="K^{-}"
  if (pp=="proton"): pp="p"
  if (pp=="neutron"): pp="n"
  if (pp=="pi0"): pp="#pi^{0}"
  if (pp=="pi-"): pp="#pi^{-}"

  # plot legend
  leg2=legends[i]
  leg2.AddEntry(f1,s1,"l")
  leg2.Draw("same");

  f1.Draw("same")
 
  #leg2.AddEntry(hh0,"<R("+pp+")>= "+str(mean0),"fl")
  #leg2.Draw("same");


  #myTextUser(0.06,0.68,1,0.1,str(e)+" GeV")
  myTextUser(18,MaxY*0.8,2,0.14,pp)

gPad.RedrawAxis()
c1.Update()


if (myinput != "-b"):
              if (input("Press any key to exit") != "-9999"):
                         c1.Close(); sys.exit(1);

