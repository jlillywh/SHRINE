from scipy.stats import gamma

alpha = 0.6374
beta = 0.3098

gamma_function = gamma(alpha, loc=0., scale=beta)
gamma_mean = gamma_function.mean()

print("The mean is " + str(gamma_mean))

