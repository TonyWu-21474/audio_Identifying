function dist = dtw(t,r)

%输入参数：t 和 r 为求相似度的两组MFCC特征矩阵
%输出参数： dist为表征相似度的最短距离
n = size(t,1);
m = size(r,1);
%帧匹配距离矩阵
d = zeros(n,m);
for i = 1:n
    A = repmat(t(i,:),m,1);
    d(i,:) = sum((A-r).^2,2);
end
% 累积距离矩阵
D =  ones(n,m) * realmax; 
D(1,1) = d(1,1);
%动态规整
for i = 2:n
    for j = 1:m
        D1 = D(i-1,j);
        if j>1
            D2 = D(i-1,j-1);
        else
            D2 = realmax;
        end
        if j>2
            D3 = D(i-1,j-2);
        else
            D3 = realmax;
        end
        D(i,j) = d(i,j) + min([D1,D2,D3]);
    end
end

dist = D(n,m);