function [result, error] = proc(sigma)
    if nargin < 1
        sigma = 2.5;
    end
    rawrssi = csvread('roomtest_rssi.csv');
    ap = csvread('roomtest_ap.csv');
    pos = csvread('roomtest_p.csv');
    m_r = size(rawrssi, 1);
    m_ap = size(ap, 1);
    mean_r = zeros(m_r/m_ap, m_ap);
    for i=1:m_r/m_ap
        mean_r(i,:) = mean(rawrssi(i*m_ap-m_ap+1:i*m_ap,:));
    end
    rssi = mean_r;
    m = size(rssi, 1);
    
    ra=-60:2.5:-40;
    rb=5:10;
    rp=0:0.5:5;
    rq=0:0.5:12;
    result = zeros(m, 6);
    for i=1:m
        y = rssi(i,:);
        max_value = 0;
        max_answer = [0 0 0 0];
        for a=ra
            for b=rb
                r = exp((a - y) / b);
                for p=rp
                    for q=rq
                        curr_value = pdf([p q], ap, r, sigma);
                        if (curr_value > max_value)
                            max_value = curr_value;
                            max_answer = [a b p q];
                        end
                    end
                end
            end
        end
        result(i,:) = [max_answer pos(i,:)];
    end
    error = sqrt(sum((result(:,3:4) - result(:,5:6)) .^ 2, 2));
end