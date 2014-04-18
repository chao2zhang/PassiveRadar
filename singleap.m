function [] = singleap()
    X = csvread('singleap.csv', 1);
    a = X(:,1);
    b = X(:,2);
    res = fit(a, b, fittype( 'a - b * log(x)' ), fitoptions('Method', 'NonlinearLeastSquares', 'StartPoint', [0 0]))
    figure('Name', 'Rssi');
    plot(res, a, b);
    
    a = X(:,1);
    b = X(:,3);
    res = fit(a, b, fittype( 'a - b * log(x)' ), fitoptions('Method', 'NonlinearLeastSquares', 'StartPoint', [0 0]))
    figure('Name', 'Snr');
    plot(res, a, b);
end