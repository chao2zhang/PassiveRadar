%% Machine Learning Online Class - Exercise 4 Neural Network Learning

%  Instructions
%  ------------
% 
%  This file contains code that helps you get started on the
%  linear exercise. You will need to complete the following functions 
%  in this exericse:
%
%     sigmoidGradient.m
%     randInitializeWeights.m
%     nnCostFunction.m
%
%  For this exercise, you will not need to change any code in this file,
%  or any other files other than those mentioned above.
%

%% Initialization
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
pause;

%% ================ Part 6: Initializing Pameters ================
%  In this part of the exercise, you will be starting to implment a two
%  layer neural network that classifies digits. You will start by
%  implementing a function to initialize the weights of the neural network
%  (randInitializeWeights.m)

fprintf('\nInitializing Neural Network Parameters ...\n')

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);

% Unroll parameters
initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];

%% =================== Part 8: Training NN ===================
%  You have now implemented all the code necessary to train a neural 
%  network. To train your neural network, we will now use "fmincg", which
%  is a function which works similarly to "fminunc". Recall that these
%  advanced optimizers are able to train our cost functions efficiently as
%  long as we provide them with the gradient computations.
%
fprintf('\nTraining Neural Network... \n')

%  After you have completed the assignment, change the MaxIter to a larger
%  value to see how more training helps.
options = optimset('MaxIter', 500);

%  You should also try different values of lambda
lambda = 1;

% Create "short hand" for the cost function to be minimized
costFunction = @(p) nnCostFunction(p, input_layer_size, hidden_layer_size, num_labels, X, y, lambda);

% Now, costFunction is a function that takes in only one argument (the
% neural network parameters)
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

% Obtain Theta1 and Theta2 back from nn_params
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), num_labels, (hidden_layer_size + 1));

fprintf('Program paused. Press enter to continue.\n');
pause;

%% ================= Part 10: Implement Predict =================
%  After training the neural network, we would like to use it to predict
%  the labels. You will now implement the "predict" function to use the
%  neural network to predict the labels of the training set. This lets
%  you compute the training set accuracy.

[pred, h] = predict(Theta1, Theta2, X);
fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);
[pred, h] = predict(Theta1, Theta2, X_test);
fprintf('\nTesting Set Accuracy: %f\n', mean(double(pred == y_test)) * 100);
errors = sqrt(sum((pos(pred, :) - pos(y_test, :)) .^ 2, 2));
h2 = h .* h;
h2 = h2 ./ (sum(h2, 2) * ones(1, size(h2, 2)));
h3 = h .* h .* h;
h3 = h3 ./ (sum(h3, 2) * ones(1, size(h3, 2)));