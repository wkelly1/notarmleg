input = readmatrix("input.txt");
output = readmatrix("output.txt");

Weight = 2*rand(1,3) - 1;

for epoch = 1:10000
    Weight = SGD_method(Weight, input, output);
end

save('Trained_Network.mat')