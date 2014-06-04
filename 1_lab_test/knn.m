rssi = csvread('roomtest_rssi.csv');
% rssi = rssi(:,[1 2 3 4 5]);
rssi = rssi(:,[4 5]) - rssi(:, 1) * ones(1, 2);
pos = csvread('roomtest_p.csv');
m = size(rssi, 1);
num_labels = 28;
num_samples = 5;
num_train = 4;
num_test = num_samples - num_train;
idx = ones(num_train, 1) * linspace(1, num_labels * num_samples - num_samples + 1, num_labels) ...
       + linspace(0, num_train - 1, num_train)' * ones(1, num_labels);
idx = reshape(idx, 1, []);
X = rssi(idx, :);
y = reshape(ones(num_train, 1) * linspace(1, num_labels, num_labels), [], 1);
idx_test = ones(num_test, 1) * linspace(1, num_labels * num_samples - num_samples + 1, num_labels) ...
       + linspace(0, num_test - 1, num_test)' * ones(1, num_labels) + num_train;
idx_test = reshape(idx_test, 1, []);
X_test = rssi(idx_test, :);
y_test = reshape(ones(num_test, 1) * linspace(1, num_labels, num_labels), [], 1);
t = size(X_test, 1);
e = zeros(t, 1);
for i = 1:t
    d = [1 + sum((X - repmat(X_test(i,:), size(X, 1), 1)) .^ 2, 2) y];
    [dummy, dex] = sort(d(:,1));
    d = d(dex,:);
    d = d(1:5,:);
    d(:,1) = 1 ./ d(:,1);
    d(:,1) = d(:,1) .^ 3;
    d(:,1) = d(:,1) ./ sum(d(:,1));
    ee = d(:,1)' * pos(d(:,2), :);
    e(i) = sqrt(sum((ee - pos(y_test(i))) .^ 2));
end