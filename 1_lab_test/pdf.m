function value = pdf(p, circles, radii, sigma)

m = size(circles, 1);
value = 0;
for i=1:m
    value = value + log(normpdf(sqrt((p(1) - circles(i,1)) * (p(1) - circles(i,1)) + (p(2) - circles(i,2)) * (p(2) - circles(i,2))), radii(i), sigma)); 
end

end