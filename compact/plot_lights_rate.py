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
nameY="Nr (#gamma)"


Xmin=0.01 
Xmax=21.
Ymin=10000 
Ymax=10000000-1000 

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
functions1=[]
functions2=[]
functions3=[]

data1=[]
data2=[]
data3=[]

# define functions
ptmin=Xmin 
ptmax=Xmax
#s1="sqrt(([0]/sqrt(x))*([0]/sqrt(x))+([1]/x)*([1]/x)+[2]*[2])"
# s1="([0]/sqrt(x))+[1]"
s1="[0]*x + [1]"

for i in range(8):
  leg2=TLegend(0.18, 0.75, 0.4, 0.92);
  leg2.SetBorderSize(0);
  leg2.SetTextFont(62);
  leg2.SetFillColor(10);
  leg2.SetTextSize(0.1);
  legends.append(leg2)

  f1=TF1("f1",s1,ptmin,ptmax);
  f1.SetLineStyle(2)
  f1.SetLineWidth(2)
  f1.SetLineColor(2)
  f1.SetParameter(0,0.5)
  f1.SetParameter(1,4.58662e-01)
  functions1.append(f1)

  scin=TGraphErrors()
  scin.SetLineColor( 1 )
  scin.SetMarkerColor( 2 )
  scin.SetMarkerSize(1)
  scin.SetMarkerStyle(21)
  data1.append(scin)

  f1=TF1("f1",s1,ptmin,ptmax);
  f1.SetLineStyle(3)
  f1.SetLineWidth(2)
  f1.SetLineColor(3)
  f1.SetParameter(0,0.5)
  f1.SetParameter(1,4.58662e-01)
  functions2.append(f1)

  scin=TGraphErrors()
  scin.SetLineColor( 1 )
  scin.SetMarkerColor( 3 )
  scin.SetMarkerSize(1)
  scin.SetMarkerStyle(20)
  data2.append(scin)

  f1=TF1("f1",s1,ptmin,ptmax);
  f1.SetLineStyle(1)
  f1.SetLineWidth(2) 
  f1.SetLineColor(4)
  f1.SetParameter(0,0.5)
  f1.SetParameter(1,4.58662e-01)
  functions3.append(f1)

  scin=TGraphErrors()
  scin.SetLineColor( 1 )
  scin.SetMarkerColor( 4 )
  scin.SetMarkerSize(1)
  scin.SetMarkerStyle(22)
  data3.append(scin)


for i in range(8):
  c1.cd(i+1);

  gPad.SetLogy(1)
  gPad.SetLeftMargin(0.15)
  print("Draw pad=",i)
  gPad.SetRightMargin(0.01);
  # second column
  if i>0:
          if (i%2 !=0): 
                     gPad.SetLeftMargin(0.11);
                     gPad.SetRightMargin(0.05);

  gPad.SetBottomMargin(0.06);
  gPad.SetTopMargin(0.005);

  if (i>5): gPad.SetBottomMargin(0.18);
  if (i<2): gPad.SetTopMargin(0.05);


  part=particles[i]

  scin=data1[i] # take a graph
  cher=data2[i] # take a graph
  scin_cher=data3[i] # take a graph

  MaxY=Ymax
  # fill this graph
  j=0
  for e in energies:
      fname="histos/hist_"+part+"_"+str(e)+"gev.root"
      xfile0=TFile( fname )
      hh=xfile0.Get("scintil")
      hh.SetDirectory(0)
      xfile0.Close()
      RMS=hh.GetRMS() # rms90(hh);
      ERR=hh.GetRMSError()
      MEAN=hh.GetMean()
      MEAN_ERROR=hh.GetMeanError()
      print(part, e,"GeV  RMS=",RMS," MEAN=",MEAN," RMS/MEAN=",RMS/MEAN)
      scin.SetPoint(j,e,MEAN)
      scin.SetPointError(j,0.0, MEAN_ERROR)


      xfile0=TFile( fname )
      hh=xfile0.Get("cherenk")
      hh.SetDirectory(0)
      xfile0.Close()
      RMS=hh.GetRMS() # rms90(hh);
      ERR=hh.GetRMSError()
      MEAN=hh.GetMean()
      MEAN_ERROR=hh.GetMeanError()
      print(part, e,"GeV  RMS=",RMS," MEAN=",MEAN," RMS/MEAN=",RMS/MEAN)
      cher.SetPoint(j,e,MEAN)
      cher.SetPointError(j,0.0, MEAN_ERROR)
       
      xfile0=TFile( fname )
      hh=xfile0.Get("scintil_cherenk")
      hh.SetDirectory(0)
      xfile0.Close()
      RMS=hh.GetRMS() # rms90(hh);
      ERR=hh.GetRMSError()
      MEAN=hh.GetMean()
      MEAN_ERROR=hh.GetMeanError()
      print(part, e,"GeV  RMS=",RMS," MEAN=",MEAN," RMS/MEAN=",RMS/MEAN)
      scin_cher.SetPoint(j,e,MEAN)
      scin_cher.SetPointError(j,0.0, MEAN_ERROR)


      #if (j==1): MaxY=(RMS/MEAN)*3 
      j=j+1

  ymin=Ymin
  ymax=Ymax
  MaxY=ymax 
  h=gPad.DrawFrame(Xmin,ymin,Xmax,ymax);
  h.Draw()
  ax=h.GetXaxis();
  ax.SetTitle( nameX );
  ay=h.GetYaxis();
  ay.SetTitle( nameY );

  ax.SetLabelSize(0.07)
  ax.SetTitleSize(0.09)
  ax.SetTitleOffset(1.0)
  ay.SetTitleOffset(1.05)

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
   
  scin.Draw("][pe same")
  f1=functions1[i]
  nn=0
  chi2min=10000
  parbest=[]
  for j in range(20):
     fitr=scin.Fit(f1,"SMR0")
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
  #s1=a1+"/ E+"+b1
  f1.Draw("same")



  # cherenkov
  cher.Draw("][pe same")
  f2=functions2[i]
  nn=0
  chi2min=10000
  parbest=[]
  for j in range(20):
     fitr=cher.Fit(f2,"SMR0")
     print "Status=",int(fitr), " is valid=",fitr.IsValid()
     if (fitr.IsValid()==True):
             chi2=f2.GetChisquare()/f2.GetNDF()
             if chi2<chi2min:
                    chi2min=chi2;
                    if nn>4:
                           break;
                    f2.SetParameter(0,random.randint(0,1))
                    f2.SetParameter(1,random.randint(0,1))
                    #f1.SetParameter(2,random.randint(0,50))
                    nn=nn+1
  fitr.Print()
  print ("Is valid=",fitr.IsValid())
  # do not show muons. They are MIP 
  #if (part != "mu-"): f1.Draw("same")

  par1 = f2.GetParameters()
  a1='%.3f'%( par1[0] )
  b1='(%.3f'%( par1[1] )+")"
  #k1='%.2f'%( par1[2] )
  #s1="#sqrt{"+a1+" ^{2} / E +"+b1+" ^{2}/E +"+k1+"^{2}}"
  #s1=a1+"/ \sqrt{E}+"+b1
  s1=a1+"/ E+"+b1
  f2.Draw("same")



  scin_cher.Draw("][pe same")
  f3=functions3[i]
  nn=0
  chi2min=10000
  parbest=[]
  for j in range(20):
     fitr=scin_cher.Fit(f3,"SMR0")
     print "Status=",int(fitr), " is valid=",fitr.IsValid()
     if (fitr.IsValid()==True):
             chi2=f3.GetChisquare()/f3.GetNDF()
             if chi2<chi2min:
                    chi2min=chi2;
                    if nn>4:
                           break;
                    f3.SetParameter(0,random.randint(0,1))
                    f3.SetParameter(1,random.randint(0,1))
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
  s1=a1+"x  E+"+b1
  f3.Draw("same")
  print("Cherenkov+scint",s1) 


 
  pp=part
  if (pp=="mu-"): pp="#mu^{-}"
  if (pp=="gamma"): pp="#gamma"
  if (pp=="kaon-"): pp="K^{-}"
  if (pp=="proton"): pp="p"
  if (pp=="neutron"): pp="n"
  if (pp=="pi0"): pp="#pi^{0}"
  if (pp=="pi-"): pp="#pi^{-}"

  # plot legend
  if (i==0):
     leg2=TLegend(0.4, 0.15, 0.8, 0.50);
     leg2.SetBorderSize(0);
     leg2.SetTextFont(62);
     leg2.SetFillColor(10);
     leg2.SetTextSize(0.1);
     leg2.AddEntry(scin,"Scint.", "p")
     leg2.AddEntry(cher,"Cherenkov", "p")
     leg2.AddEntry(scin_cher,"Scint+Cherenk", "p")
     leg2.Draw("same");

  #leg2.AddEntry(f1,s1,"l")
  #if (part != "muon"): leg2.Draw("same");
 
  #leg2.AddEntry(hh0,"<R("+pp+")>= "+str(mean0),"fl")
  #leg2.Draw("same");


  #myTextUser(0.06,0.68,1,0.1,str(e)+" GeV")
  xpos=ymin+0.1 
  if (xpos>0.89): xpos=0.93
  myTextUser(18,xpos,2,0.14,pp)

gPad.RedrawAxis()
c1.Update()


if (myinput != "-b"):
              if (input("Press any key to exit") != "-9999"):
                         c1.Close(); sys.exit(1);

