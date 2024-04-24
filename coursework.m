%% Applied statistics courswork


%% Q1A)

%T test becausw we dont have standard deviation 
% defining the parameters in the question
n = 100; 
r = 0.4;
alpha = 1; 
num_samples = 1000; 

% Simulation of Y
Y = zeros(1, num_samples); 
for i = 1:num_samples
    intervals = exprnd(1/r, n, 1); % generating exponential random variables
    Y(i) = max(intervals); % Maximum interval observed
end

% Plotting distributions
figure;
subplot(1,2,1);
histogram(Y, 'Normalization', 'pdf');
title('Empirical Distribution of Y');
xlabel('Time intervals');
ylabel('Probability Density');

subplot(1,2,2);
cdfplot(Y);
title('Empirical Cumulative Density Function of Y');
xlabel('Time intervals');
ylabel('Cumulative Probability');
%----------------------------------------

%% Q1B)

%N A t-test is generally used to compare the means of two groups or to compare a single group's 
% mean against a known value. 
% The maximum observed time interval, Y, might not follow a normal distribution, which 
% is a key assumption of the t-test.

%If we are interested in testing whether 
% the average maximum observed time interval exceeds a specific threshold, 
% consider using a one-sample t-test. This assumes the data is approximately normally 
% distributed or that the sample size is large enough for the Central Limit Theorem to justify 
% the approximation.

% Parameters have already been defined

%Some of the reasons for using hypothesis testing on simulated data include: 
% confirming or reject theories or results by generating data with known properties.
%, Explore how changes in data characteristics affect the outcomes of hypothesis tests.
%and ensuring that statistical methods work as expected under various scenarios, including extreme
% cases that might not necasserily always arise in real data. These
% extremeties might affect the hypothesis test.


% Simulation of Y
Y = zeros(1, num_samples); 
for i = 1:num_samples
    intervals = exprnd(1/r, n, 1); % Generate exponential random variables
    Y(i) = max(intervals); % Maximum interval observed
end

%  t-Test
threshold = 4; % Threshold time interval (4 seconds)
[h, p, ci, stats] = ttest(Y, threshold, 'Tail', 'right'); % One-sample t-test with right tail

% Results 
fprintf('Alternative Hypothesis: Mean maximum interval > 4 seconds\n');
fprintf('Test Result (h): %d (1=reject null, 0=fail to reject null)\n', h);
fprintf('95%% Confidence Interval of the Mean: [%.3f, %.3f]\n', ci);
disp(stats)

%% Q1C)

num_samples = length(Y);
num_bootstrap = 500;
means = zeros(num_bootstrap, 1); %array for mean of each bootstrap sample

% Generate bootstrap samples and compute their means
for i = 1:num_bootstrap
    sample_indices = randi(num_samples, num_samples, 1);  % Random indices with replacement
    bootstrap_sample = Y(sample_indices);         
    means(i) = mean(bootstrap_sample);          
end

lower = quantile(means, 0.005);
upper = quantile(means, 0.995);

% Display the results
fprintf('99%% Bootstrap Confidence Interval for the mean of Y: [%.2f, %.2f]\n', lower, upper);

% - Using bootstrapping for constructing confidence intervals in this scenario 
%   can be effective as it does not rely on the assumptions of the underlying distribution of 
%   the data. 
% - Bootstrapping handles small samples well which may be good for
% something likethis question when we have 500 samples.
% 

%% Q1D)

% Adjusted simulation for changing rate
new_r = [0.4 * ones(500,1); 1.0 * ones(500,1)]; 
Y_adjusted = zeros(1, num_samples);
for k = 1:num_samples
    intervals_adjusted = exprnd(1./new_r);
    Y_adjusted(k) = max(intervals_adjusted);
end

% Plot for the adjusted rate scenario
figure;
subplot(1,2,1);
histogram(Y_adjusted, 'Normalization', 'pdf');
title('Adjusted Rate: Empirical Distribution of Y');
xlabel('Time intervals');
ylabel('Probability Density');

subplot(1,2,2);
cdfplot(Y_adjusted);
title('Adjusted Rate: Empirical CDF of Y');
xlabel('Time intervals');
ylabel('Cumulative Probability');

%-------------------------------------------------

%% Q1E)


% Objective function to minimize (negative log-likelihood)
objectiveFunction = @(params) -sum(log(params(1)/sqrt(2*pi*params(3)^2) * exp(-(Y_adjusted-params(2)).^2/(2*params(3)^2)) + ...
                                  (1-params(1))/sqrt(2*pi*params(5)^2) * exp(-(Y_adjusted-params(4)).^2/(2*params(5)^2))));

% Initial guesses for parameters: [p1, mu1, sigma1, mu2, sigma2]
initialParams = [0.5, mean(Y_adjusted), std(Y_adjusted), mean(Y_adjusted), std(Y_adjusted)];

% Optimisation using fminsearch
options = optimset('Display', 'iter');
bestParams = fminsearch(objectiveFunction, initialParams, options);

% Display the best fit parameters
fprintf('Best fit parameters: p1 = %.2f, mu1 = %.2f, sigma1 = %.2f, mu2 = %.2f, sigma2 = %.2f\n', ...
        bestParams(1), bestParams(2), bestParams(3), bestParams(4), bestParams(5));


%% Q1F)

%  - Central limit theorem says that the average of a large number of independent, 
% identically distributed variables with finite means and variances will 
% approximately follow a normal distribution, regardless of the underlying 
% distribution.

% - The measurements (time intervals) must be independent across counters.
%The counters should operate under the same conditions and hence have 
% identically distributed measurement times.

% - Alpha (transmission success probability) and theta(parameters of the distribution 
% of time intervals) could affect the  identical distribution assumption if they 
% vary among counters. Variability in alpha and theta would introduce heterogeneity in the data, 
% potentially violating the conditions under which the CLT applies.


% End of question 1--------------------------------------------------------


%% Q2A)

% preprocess data and load into years and consumption
data = importdata('coursework_data.txt');

years = data.data(1, 2:end)'; 
consumption = data.data(2, 2:end)'; 

% indices for years after and before 1960
after_1960 = years >= 1960;
before_1960 = years < 1960;

% extracting the data for years after and before 1960
years_after_1960 = years(after_1960);
consumption_after_1960 = consumption(after_1960);
years_before_1960 = years(before_1960);
consumption_before_1960 = consumption(before_1960);

% fitting linear models
model_after_1960 = fitlm(years_after_1960, consumption_after_1960);
model_before_1960 = fitlm(years_before_1960, consumption_before_1960);

% Generate fitted values using the linear models specifically for their respective year ranges
fitted_after_1960 = predict(model_after_1960, years_after_1960);
fitted_before_1960 = predict(model_before_1960, years_before_1960);

% figures
figure;
scatter(years_before_1960, consumption_before_1960, 'b', 'filled');
hold on;
scatter(years_after_1960, consumption_after_1960, 'r', 'filled');
plot(years_before_1960, fitted_before_1960, 'b-', 'LineWidth', 2); % Plot only before 1960
plot(years_after_1960, fitted_after_1960, 'r-', 'LineWidth', 2); % Plot only starting from 1960
hold off;
xlabel('Year');
ylabel('Average per capita consumption (kg)');
title('Average per capita consumption of crystallised sugar in Great Britain');
legend('Data Before 1960', 'Data After 1960', 'Linear Fit Before 1960', ...
    'Linear Fit After 1960', 'Location', 'best');
grid on;


%% Q2B)

% Display the coefficients for the models
disp('Coefficients for the model before 1960:');
disp(model_before_1960.Coefficients);
disp('Coefficients for the model after 1960:');
disp(model_after_1960.Coefficients);

%Model Before 1960:
%Intercept : -832.07
%negative value suggests a non-physical result when extrapolated far back beyond the data range, 
% indicating the model's limitations for historical predictions.
%Slope : 0.45672 
%Indicates a statistically significant increase in sugar consumption of about 0.457 kg per capita 
% per year before 1960 (p-value: 2.058e-56).
%Reflects rising trends in sugar intake

%Model After 1960:
%Intercept : 1064.7
%High baseline sugar consumption at the start of this period, significantly
%higher than the historical average.
%Slope : -0.51276 :
%Shows a statistically significant decrease in sugar consumption of about 0.513 kg per capita 
% per year after 1960 (p-value: 9.9065e-16).
%Suggests a reversal in consumption trends. Again could be problematic when
%extrapolating into the future.


%% Q2C)

figure;
subplot(2,2,1)
plotResiduals(model_before_1960)
title('Residuals Normality Before 1960');
subplot(2,2,2)
plotResiduals(model_before_1960,'probability')
title('Residuals Probability Before 1960');
subplot(2,2,3)
plotResiduals(model_before_1960,'fitted')
title('Residuals vs. Fitted Before 1960');
subplot(2,2,4)
plotResiduals(model_before_1960,'lagged')
title('Residuals Lagged Before 1960');

sgtitle('Residuls for original model before 1960'); % Super title for the entire figure

figure;
subplot(2,2,1)
plotResiduals(model_after_1960)
title('Residuals Normality After 1960');
subplot(2,2,2)
plotResiduals(model_after_1960,'probability')
title('Residuals Probability After 1960');
subplot(2,2,3)
plotResiduals(model_after_1960,'fitted')
title('Residuals vs. Fitted After 1960');
subplot(2,2,4)
plotResiduals(model_after_1960,'lagged')
title('Residuals Lagged After 1960');

sgtitle('Residuls for original model after 1960'); 

%The histogram of residuals before 1960 does not quite follow the bell curve 
% expected from a normal distribution suggesting that they do not follow a 
% normal distribution. For an appropriate model, residuals should be 
% approximately normally distributed. The deviation implies that the linear
% model might not be capturing some systematic variance in the data.

%Again the Q-Q plot for before 1960 should ideally show the residuals 
% falling along the straight diagonal line, which would indicate that the 
% residuals are normally distributed. The fact that the tails of the plot 
% tend to skew from the line, indicates that the residuals have a distribution 
% with heavier tails than the normal distribution. This could indicate that the 
% linear model is not captured the full patterns, however if these are 
% outliers then that could also be the cause.

%For the residuals vs fitted value the plot should look random which it does 
% so there are not many conclusions that can be draw from this. 

%From this it can be concluded that the through analysiing the residual plots 
% of the data after 1960 the liner model captures the trends quite well although 
% it may be suitable to use a quadratic model for to capture the trends before 1960.


%From plotting the residuls we can see that the data for after 1960 looks
%good and follows the a normal distribution however this is not the case
%for the data before 1960. For this reason we can make some improvements by
%fitting a quadratic model instead.

% Create a new table including the year, its square, and the consumption
tbl_before_1960 = table(years_before_1960, years_before_1960.^2, consumption_before_1960, ...
                        'VariableNames', {'Year', 'YearSquared', 'Consumption'});

% Fit a quadratic model
quad_before_1960 = fitlm(tbl_before_1960, 'Consumption ~ Year + YearSquared');

% Display the model summary
disp(model_before_1960);


subplot(2,2,1)
plotResiduals(quad_before_1960)
title('Residuals Normality Before 1960');
subplot(2,2,2)
plotResiduals(quad_before_1960,'probability')
title('Residuals Probability Before 1960');
subplot(2,2,3)
plotResiduals(quad_before_1960,'fitted')
title('Residuals vs. Fitted Before 1960');
subplot(2,2,4)
plotResiduals(quad_before_1960,'lagged')
title('Residuals Lagged Before 1960');

sgtitle('Residuls for improved quadratic model before 1960'); 




%% Q2D)

% To find the point where sugar was first consumed we can do a simple 
% calculation to find the roots of the quadratic from the improved model in 
% section above. To find the point where sugar was first consumed would be
% when the y intecept is 0(root) and from this we would want to pick the
% smaller of the roots because the question is asking us for the first year
% that sugar was consumed.

coeffs = table2array(quad_before_1960.Coefficients(:, 'Estimate'));
a = coeffs(3); % Coefficient of Year^2
b = coeffs(2); % Coefficient of Year
c = coeffs(1); % Intercept

% discriminant calculation
discriminant = b^2 - 4*a*c;

% making sure the discriminant is not negative which indicated no roots 
if discriminant >= 0
    t1 = (-b + sqrt(discriminant)) / (2*a);
    t2 = (-b - sqrt(discriminant)) / (2*a);
    % Because we want when sugar was first consumed we want the smaller
    % root
    firstYear = min(t1, t2); % using the min function to find the smallest root
    if firstYear < min(years_before_1960)
        fprintf('Estimated first year of sugar consumption: %f\n', firstYear);
    else
        fprintf('Extrapolation does not produce a realistic result within the data range.\n');
    end
else
    fprintf('No real roots, the model does not intersect the consumption axis at zero.\n');
end

%% Q2E)

% Prior to 1960, the industrial revolution and subsequent 
% developments might have led to increased sugar consumption due to mass 
% production of food products. This period likely saw the introduction and 
% growth of processed foods, which tend to contain higher sugar levels. 
% During this time a lack of widespread public health 
% awareness of sugar likely made the sugar consumption increase further.
% This would cause a steeper gradient and hence the y intercept would be
% much later than it should be.

% Before this time(many years before the 1900s) it is plausible that the trend upwards in terms 
% of sugar
% consumption was much lower as it was less readily available in the same
% quantity due to less processed foods and drinks.


% While quadratic models can capture certain 
% trends within the data range they are applied to, they are limited by 
% their inability to incorporate external factors such as public health 
% trends, economic conditions, and cultural shifts unless explicitly included 
% through additional data and variables. This mean thats it is plausible to
% see the massive discrepenancy between the predicted values and the actual
% known value.

% End of quesion 2---------------------------------------------------------


%% Q3A)

A = importdata("coursework_data.txt");

x = A.data(1, :)'; 
y = A.data(2, :)';  


x2 = zeros(length(x), 1);
x2(1:95) = 0;
x2(96:end) = 1;


data = table(x, x2, y, 'VariableNames', {'x','x2','y'});
data.x2 = nominal(data.x2);
single_model = fitlm(data, 'y~x*x2');

figure; 
scatter(x, y, 'filled'); 
hold on; 

y_pred = predict(single_model, data);


plot(x, y_pred, 'b-', 'LineWidth', 2); 

xlabel('X variable');
ylabel('Dependent variable (Y)');
title('Scatter Plot with Fitted Regression Line');
legend('Data', 'Fitted Line', 'Location', 'best');
grid on;
hold off; % 


disp(single_model)

%% Q3B)

% For the next part of the question we can compare certain metrics to
% determine which of the models is more appropriate 

fprintf('Before 1960')
disp(model_before_1960)
fprintf('After 1960')
disp(model_after_1960)
fprintf('Single model')
disp(single_model)

%The intercept in the single model (-826.05) is very close to the intercept 
% of the separate model before 1960 (-832.07).
%The slope in the single model for x when x2 is 0 (0.4535) 
% is also very close to the slope of the separate model  before 1960 (0.45672).

%For the separate model after 1960 we need to a few calculations to work out the adjusted 
% intercept and slope to assess the single model.

%Given the values: Intercept (1064.7) and Slope (-0.51276)

%Adjusted Intercept for after 1960: -826.05 + 1906.8 = 1080.75
%Adjusted Slope for after 1960: 0.4535 - 0.97425 = -0.52075
%These values computed from the single model are:

%The adjusted intercept (1080.75) is very close to the intercept from the separate model (1064.7).
%The adjusted slope (-0.52075) is close to the slope from the separate model (-0.51276).
%Conclusion
%The coefficients of the single model effectively encapsulate the effects seen in the two 
% separate models with very minor discrepancies, possibly due to rounding or the fitting 
% procedure considering the entire data at once. The interaction term in the single model 
% adjusts the slope and intercept precisely to match what is observed when modeling the two 
% periods separately, thereby providing a consistent and integrated view of how the relationship 
% between x and y changes across the breakpoint of 1960.



%% Q3C)

%For a start the models are differenet in the fact that one of them is one
%continuous model across the full dataset and the one in question 2 is too
%individual model fitting to different parts of the dataset.

% If there's a clear breakpoint that splits the 
% dataset into two distinct groups, and these groups have different trends
% relationships, two models is most likely the better choice.


% When a variable transitions between conditions are not abrupt, a single 
% model with interaction terms is beneficial. It can reveal how relationships 
% shift in response to changes in another variable.

% In this example looking at the plot it is clear to see that the change of
% sugar consumption changes very abruptly and the relationships between the
% independent variable(time) and dependent(sugar consumption) are very
% different. However from the previous question it can be observed that the
% deviation between the both models is very small and both yield very
% similar results. 

%for this reason i think using the single model is more beneficial because
% it simplifies the analysis by using one continuous model but also gives us 
% a clear mathematical relationship to switch between conditions as opposed
% to the two seperate models that dont allow such a seemless switch.

% End of question 3 -------------------------------------------------------


%% Q4i)
% Parms

n=2000;

x = 5*rand(1, n)';
z = 5*rand(1, n)';

n = length(x); 


lambda = 2 + 1.5*x + 0.6*z + 0.5*x.*z; 

% Generate y
y = random('Exponential', 1./lambda, [n, 1]); 

% table
toy = table(x, z, y, 'VariableNames', {'x', 'z', 'y'}); % Correct the order and spelling

% model
m = fitglm(toy, 'y ~ x * z', 'Distribution', 'gamma'); % Adding a link function


% Stastical analysis

%  - All predictors including the interaction term have 
% p-values well below the 0.05 threshold, indicating that they are statistically significant. 

%  - The F-statistic against the constant model is high, and the associated 
% p-value is extremely low, suggesting the model is strong. 
% 
%  - The estimated dispersion is close to 1 and suggests that the variance is appropriately 
% accounted for in the model.

% Shortcomings:

%  - Orginal Model does not show dispersion of f statistic which are
%   valuable model metrics to determine the performance and suitablilty of
%   the model. For example the Gamma distribution has a variance that is a function of the mean.
%   The dispersion parameter can tell us whether this relationship is being properly accounted for 
%   in the model.

% - Stating that "for every unit increase in x, the response y increases by
%   1.5 units" is not true. The statement "for every unit increase in x, the response
%   y increases by 1.5 units" implies a simple linear relationship, but this is only accurate 
%   in the absence of interaction terms. This is only true only when z is held constant. 

%  - It is stated int the question that the data is known to come from an exponential distribution, 
%   but the model is fitted with a Gamma distribution.


% integrating improvements 

disp(m)
% displaying the model from the toy dataset gives us access to the f
% statistic and dispersion from recreating the analysis



%% Q4ii)

n= 1000;
x = linspace(-1,1, n)';
epsilon = random('Normal',0,0.1.*x.^2);
y = 0.2*(x.^3) + epsilon;
data = table(x,y);
m = fitlm(data, 'y~x');


subplot(2,2,1)
plotResiduals(m)
title('Residuals Normality');
subplot(2,2,2)
plotResiduals(m,'probability')
title('Residuals Probability');
subplot(2,2,3)
plotResiduals(m,'fitted')
title('Residuals vs. Fitted');
subplot(2,2,4)
plotResiduals(m,'lagged')
title('Residuals Lagged');
 
%discuss the fit 

% Good practices 

% - Diagnostic Plots: The use of multiple residual diagnostic plots is good 
% statistical practice. It helps to assess the assumptions of the linear regression 
% model.

% - Normality : The histogram and normal probability plot (Q-Q plot) are 
% used to check the normality of residuals, which is a key assumption of 
% linear regression.

% - Homoscedasticity : The plot of residuals versus fitted values 
% is used to check for constant variance (homoscedasticity) across the range 
% of predictions.

% Statisitcal results:

% - The histogram shows that the residuals are roughly bell-shaped but seem 
% slightly skewed.

% - The normal probability plot indicates some deviation from normality, 
% particularly in the tails.

% - The residuals versus fitted values plot shows a clear pattern. 
% This suggests the presence of heteroscedasticity, which violates the 
% assumption of constant variance.

% - The residuals lagged plot a clumping of datapointsinstead of a random 
% cloud. This implies that the residuals are not independent, violating 
% another regression assumption.


% Shortcomings:

% - The relationship being modelled as linear is incorrect as discussed above. 
% A polynomial or a non-linear model could be more suitable 

% - When the model fails to capture the true relationship, 
% the estimates of the model coefficients are biased. This means they do not 
% reflect the true effects of the predictors on the response variable.

% - Even if the model is unbiased, non-linear patterns in residuals 
% can lead to inefficiencies in the estimates, reducing the usefullness of 
% the model.

% - Thee standard statistical tests for 
% coefficients (like t-tests) assume that the model correctly specifies the 
% form of the relationship between predictors and the response. Non-linearity 
% can lead to invalid p-values and confidence intervals

%Improvements:


% - We could fit a number of different models such as one that contains 
% polynomial terms to better fit to the non linear data 

%integtrated improvements 

% Fit a quadratic model
qm = fitlm(data, 'y ~ 1 + x + x^2');



%% Q4iii)


A_flips = 20;  % number of flips for coin A
P_of_A = 0.8; % Probability of heads for coin A
B_flips = 40;  % Number of flips for coin B
P_of_B = 0.6; % probability of heads for coin B

% toy dataset outcomes for each coin
% Coin A: 1 for heads, 0 for tails
outcomesA = rand(1, A_flips) < P_of_A;
% Coin B: 1 for heads, 0 for tails
outcomesB = rand(1, B_flips) < P_of_B;

% Calculate the proportions of heads in the generated outcomes
proportionA = sum(outcomesA) / A_flips;
proportionB = sum(outcomesB) / B_flips;

% Display the proportions for both coins
fprintf('Proportion of heads for coin A: %.2f\n', proportionA);
fprintf('Proportion of heads for coin B: %.2f\n', proportionB);

% Combine outcomes for randomization test
combinedOutcomes = [outcomesA, outcomesB];
observedDifference = proportionB - proportionA;

% randomisation test
S = 2000;  % permutations, this has been increased to account for the improvements section
differences = zeros(1, S);
for i = 1:S
    permuted = combinedOutcomes(randperm(A_flips + B_flips));
    permutedA = permuted(1:A_flips);
    permutedB = permuted(A_flips + 1:end);
    differences(i) = (sum(permutedB) / B_flips) - (sum(permutedA) / A_flips);
end

% Calculate the p-value for a two-tailed test

extremeLower = sum(differences <= observedDifference); % Count lower extremes
extremeUpper = sum(differences >= observedDifference); % Count upper extremes
pValue = (extremeLower + extremeUpper) / S; % Combine counts for both tails


% Plotting the results
figure;
subplot(1,2,1); % First subplot for proportions
bar([1 2], [proportionA proportionB], 0.5);
set(gca, 'XTickLabel', {'Coin A', 'Coin B'}, 'XTick', 1:2);
ylabel('Proportion of Heads');
title('Proportions of Heads for Coin A and B');
grid on;

subplot(1,2,2); % Second subplot for permutation test results
histogram(differences, 'FaceColor', 'blue');
hold on;
line([observedDifference observedDifference], ylim, 'Color', 'red', 'LineWidth', 2);
xlabel('Test statistics');
ylabel('Frequency');
title('Permutation Test Results');
legend('Permutation Differences', 'Observed Difference');
grid on;
text(observedDifference, max(ylim())*0.9, sprintf('p=%.4f', pValue), 'Color', 'red');

% Adjust figure properties for better visibility
set(gcf, 'Position', [100, 100, 1000, 400]); % Resize figure to avoid overlap

% Display p-value and observed difference
fprintf('Observed difference in proportions: %.4f\n', observedDifference);
fprintf('P-value from the permutation test: %.4f\n', pValue);


% Good Practice: 

% The simulation and randomisation test do not rely on the assumption of 
% normality, making them robust for small sample sizes or non-normal data. 
% The use of a p-value provides a clear criteria for statistical 
% significance.

% Shortcomings:

% - Multiple comparisons or tests increase the chance of type I error (
% false positives)

% - Not enough permutations,. Using a relatively low number of permutations, 
% such as 500, might not represent the entire permutation distribution. 
% This is especially emphasised when  the difference between the coin probabilities 
% is small.

% - Improvements:

% - increase the permutations 

% - We could use bootstrapping to create confidence intervals provide a 
% range within which the test statistic is expected to lie with a certain 
% level of confidence .  This approach assumes that the distribution of the 
% difference in proportions under the null hypothesis is symmetric and can 
% be used to estimate the variability around the observed difference under 
% the assumption that the null hypothesis is true.'





