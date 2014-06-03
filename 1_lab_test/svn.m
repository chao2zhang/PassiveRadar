clear ; close all; clc

%% Setup the parameters you will use for this exercise


%% =========== Part 1: Loading and Visualizing Data =============
% Load Training Data
fprintf('Loading data ...\n')

rssi = csvread('roomtest_rssi.csv');
ap = csvread('roomtest_ap.csv');
pos = csvread('roomtest_p.csv');
m = size(rssi, 1);
input_layer_size = 5;
hidden_layer_size = 50;
num_labels = 28;
num_samples = 5;
num_train = 3;
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
pause;