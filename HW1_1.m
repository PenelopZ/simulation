% MSCS 6020 
% Homework 1
% Shengya Zhang

% Pseudorandom number generator

A=zeros(10000,1);
XP=5;
m=2^31-1;
a=7^5;
% First 10 iteration
for i=1:1:10
    
    XN=mod(3*XP,150);
    fprintf('X%d is: %d\n',i,XP)
    XP=XN;
    
end

for i=1:1:10000
    
    XN=mod(3*XP,150);
    XP=XN;
    A(i)=XN;
end

A_Mean=mean(A)
A_Variance=var(A)

% Matlab built in function for random number and mean, variance
B=rand(10000,1);
B_Mean=mean(B);
B_Variance=var(B);
fprintf('Mean from algorithm is : %d\n',A_Mean);
fprintf('Variance from algorithm is : %d\n',A_Variance);
fprintf('Mean from Matlab is : %d\n',B_Mean);
fprintf('Variance from Matlab is : %d\n',B_Variance);
%Plot
HA=histogram(A);
figure;
HB=histogram(B);



