rf = csvread('rf.csv', 1, 0);
rf = sort(rf);
for i=1:7
    quant(rf(:,i))
end
h = stairs(y, rf(:, 1:4))
view(90, -90)
set(h(1), 'LineStyle', ':')
set(h(2), 'LineStyle', '-.')
set(h(3), 'LineStyle', '--')
legend('2AP', '3AP', '4AP', '5AP')
xlabel('CDF')
ylabel('Error(m)')