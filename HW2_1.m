% MSCS 6020 
% Homework 2
% Question 1
% Shengya Zhang

clear all

n=1000;
U=rand(n,1);, X2=zeros(n,1);
for j=1:n
if (U(j,1)<(1/3))
X(j,1)=0;
else
X(j,1)=1;
end
end

Rate1=0;
for i=1:n
    if(X(i,1)==1)
    Rate1=Rate1+1;
    end
end
Rate1=Rate1/n


MatlabR1=(binornd(1000,2/3))/1000

n2=10000;
U2=rand(n2,1);, X2=zeros(n2,1);
for j=1:n2
if (U2(j,1)<(1/3))
X2(j,1)=0;
else
X2(j,1)=1;
end
end

Rate2=0;
for i=1:n2
    if(X2(i,1)==1)
    Rate2=Rate2+1;
    end
end
Rate2=Rate2/n2

MatlabR2=(binornd(10000,2/3))/10000


