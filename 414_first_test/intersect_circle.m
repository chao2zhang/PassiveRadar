function [intersected, center_position] = intersect_circle(circles)
    m = size(circles, 1);
    p = zeros(m * (m - 1) / 2, 2);
    p_count = 0;
    function in = inside_all(p, circles)
        in = 1;
        for q=1:size(circles,1)
            if (p(1) - circles(q,1)) ^ 2 + (p(2) - circles(q,2)) ^ 2 > circles(q,3) ^ 2
                in = 0;
                break;
            end
        end
    end
    for i=1:m
        for j=i+1:m
            [p1, p2] = circcirc(circles(i,1), circles(i,2), circles(i,3), circles(j,1), circles(j,2), circles(j, 3));
            if ~any(isnan(p1)) && inside_all(p1, circles)
                p_count = p_count + 1;
                p(p_count,:) = p1;
            end
            if ~any(isnan(p2)) && inside_all(p2, circles)
                p_count = p_count + 1;
                p(p_count,:) = p2;
            end
        end
    end
    intersected = p_count > 0;
    center_position = mean(p(1:p_count, :), 1);
end