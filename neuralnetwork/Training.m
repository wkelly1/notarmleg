input = readmatrix(filename);
output = readmatrix(filename);

Weight = 2*rand(1,3) - 1;

for epoch = 1:10000
    Weight = SGD_Method(Weight, input, output);
end

save('Trained_Network.mat')