% MSCS 6020 
% Homework 2
% Question 3
% Shengya Zhang

n=1000;
U=rand(n,1);
E=0;
for j=1:n
    x=U(j,1);
    a=(1/((2*pi)^0.5))*(exp(-0.5*(x^2)));
    E=E+x*a;
end

E=E+0
