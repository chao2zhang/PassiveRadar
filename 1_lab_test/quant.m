function j = quant(m)
    j = [quantile(m, 0.25) quantile(m, 0.5) quantile(m, 0.75)];
end