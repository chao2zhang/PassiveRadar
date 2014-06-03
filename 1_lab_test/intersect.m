function [result, error] = intersect(range_q, n, ap_index)
    rawrssi = csvread('roomtest_rssi.csv');
    ap = csvread('roomtest_ap.csv');
    pos = csvread('roomtest_p.csv');
    m_r = size(rawrssi, 1);
    m_ap = size(ap, 1);
    mean_r = zeros(m_r/m_ap, m_ap);
    for i = 1:m_r/m_ap
        mean_r(i,:) = mean(rawrssi(i * m_ap - m_ap + 1: i*m_ap, :));
    end
    rssi = mean_r;
    m = size(rssi, 1);
    
    if nargin < 1
        range_q = -60:0.05:-40;
    end
    if nargin < 2
        n = 7;
    end
    if nargin < 3
        ap_index = 1:m_ap;
    end
    
    result = zeros(m, 6);
    for i = 1:m
        y = rssi(i, :);
        predicted = zeros(1, 2);
        for q = range_q
            c = [ap exp((q - y')/n)];
            x = intersect_circle(c(ap_index,:));
            if ~any(isnan(x))
                predicted = x;
                break
            end
        end
        result(i,:) = [q n predicted pos(i,:)];
    end
    error = sqrt(sum((result(:,3:4) - result(:,5:6)) .^ 2, 2));
end