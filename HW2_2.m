% MSCS 6020 
% Homework 2
% Question 2
% Shengya Zhang

clear all
close all

n=1000;
U=rand(n,1); X=zeros(n,1);
for j=1:n
if (0<=U(j,1))&(U(j,1)<.15)%P=0.15
X(j,1)=4;
elseif(.15<=U(j,1))&(U(j,1)<.35)%P=0.2
X(j,1)=2;
elseif(.35<=U(j,1))&(U(j,1)<0.65)%P=0.3
X(j,1)=1;
elseif(.65<=U(j,1))%P=0.35
X(j,1)=3;
end
end
P1=0;
P2=0;
P3=0;
P4=0;
for i=1:n
    if(X(i,1)==1)
        P1=P1+1;
    elseif(X(i,1)==2)
        P2=P2+1;
    elseif(X(i,1)==3)
        P3=P3+1;
     elseif(X(i,1)==4)
        P4=P4+1;
    end
end
P1=P1/n
P2=P2/n
P3=P3/n
P4=P4/n



