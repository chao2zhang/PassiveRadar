function [result] = proc_test1()

X = csvread('test1.csv', 1);
Y = [grpstats(X(:,[3 4]), X(:,[5 6 1 2]), 'mean') unique(X(:,[5 6 1 2]), 'rows')];
Y = Y(Y(:,6)~=2,:);
ap_position = [0 3; 3.9 0; 0 0; 3.9 3];
n = size(ap_position, 1);
m = size(Y, 1) / n;
result = zeros(m, 5);
for i=1:m
    y = [Y(n*i-n+1:n*i,1:4) ap_position];
    max_value = 0;
    max_answer = [0 0 0];
    for a=-40:-25
        for b=6:8
            r = exp((a - y(:, 1)) / b);
            for p=-5:0.5:20
                for q=-10:0.5:10
                    curr_value = pdf([p q], ap_position, r, 2.5);
                    if (curr_value > max_value)
                        max_value = curr_value;
                        max_answer = [a p q];
                    end
                end
            end
        end
    end
    result(i,:) = [max_answer Y(n*i,3:4)];
% method for intersection of circle
%     point = zeros(1, 2);
%     for a=-37:0.2:-25
%         c = [ap_position exp((a - y(:, 1))/b)];
%         [intersected, center_point] = intersect_circle(c);
%         if intersected
%             point = center_point;
%             break
%         end
%     end
%     result(i,1)=a;
%     result(i,2:3)=point;
%     result(i,4:5)=Y(n*i,3:4);
end

end

