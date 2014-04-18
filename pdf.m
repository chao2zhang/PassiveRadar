function [value] = pdf(p, circles, radii, sigma)

m = size(circles, 1);
value = 0;
for i=1:m
    value = value + normpdf(sqrt(sum((p - circles(i,:)) .^ 2)), radii(i), sigma); 
end

end