from types import SimpleNamespace
import numpy as np
class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()
        self.results = []

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3
        par.p2 = 1


        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

    def utility_A(self,x1A,x2A):
        return x1A**(self.par.alpha)*x2A**(1-self.par.alpha)

    def utility_B(self,x1B,x2B):
        return x1B**(self.par.beta)*x2B**(1-self.par.beta)
    
    ## for the first plot in question 1
    def is_pareto(self, x1A, x2A):
        x1B, x2B = 1 - x1A, 1 - x2A
        utility_personA = self.utility_A(self.par.w1A, self.par.w2A)
        utility_personB = self.utility_B(1-self.par.w1A, 1-self.par.w2A)
        return (self.utility_A(x1A, x2A) >= utility_personA and
        self.utility_B(x1B, x2B) >= utility_personB)
    

    
    def demand_A(self,p1):
        demand_x1 =  self.par.alpha * (p1*self.par.w1A + self.par.w2A)/p1  
        demand_x2 = (1-self.par.alpha) * (p1*self.par.w1A + self.par.w2A)
        return demand_x1, demand_x2
    def demand_B(self,p1):
        demand_x1 = self.par.beta * (p1* (1-self.par.w1A) + 1- self.par.w2A)/p1 
        demand_x2 = (1-self.par.beta) *(p1* (1-self.par.w1A) + (1-self.par.w2A))
        return demand_x1, demand_x2
    
    # Check for Pareto improvements
    #def is_pareto_improvement(self, xA1, xA2, x1B, x2B):
     #   return self.utility_A(self, xA1, xA2) >= self.utility_A(self,x1A = par.w1A, x2A = par.w2A) and\
     #   self.utility_B(self, x1B, x2B) >= self.utility_B(self, x1B = 1-par.w1A, x2B = 1-par.w2A)

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2

## negative utility function defined
    
    def negative_utility_A(self,p1):
        x1 = 1 - (self.par.beta * (p1* (1-self.par.w1A) + 1- self.par.w2A)/p1)
        x2 = 1 - ((1-self.par.beta) *(p1* (1-self.par.w1A) + (1-self.par.w2A)))
        negative_utility = -(x1**(self.par.alpha)*x2**(1-self.par.alpha))
        return negative_utility
    

    def negative_utility_A_5b(self, x): 
        x1A = x[0]
        x2A = x[1]
        return -(x1A**(self.par.alpha)*x2A**(1-self.par.alpha))


    def aggregate_utility(self, x): ## for task 6a 
        xA1 = x[0]
        xA2 = x[1]
        return -(self.utility_A(xA1, xA2) + self.utility_B(1 - xA1, 1 - xA2))

    def solve_3(self, p1_guess=1.0, tolerance=1e-3): # Set default values for p1_guess and tolerance
        clearing_prices = []
        min_combined_error = float('inf')
        price = None
        min_eps1 = None
        min_eps2 = None

        while p1_guess >= 0: # Loop over different values of p1 in the range [0, 1] with 75 intervals
            eps1, eps2 = self.check_market_clearing(p1_guess)
            if abs(eps1) < tolerance and abs(eps2) < tolerance: # Check if the market clears
                clearing_prices.append(p1_guess)
                combined_error = eps1**2 + eps2**2
                if combined_error < min_combined_error: # Check if the combined error is less than the minimum combined error found so far
                    min_combined_error = combined_error
                    price = p1_guess
                    min_eps1 = eps1
                    min_eps2 = eps2
            p1_guess -= 0.001 # Update the value of p1_guess

        # Print the results
        if clearing_prices:
            print(f"Minimum combined error: {min_combined_error:.5f} at price: {price:.5f}")
            print(f"Epsilon1: {min_eps1:.5f}, Epsilon2: {min_eps2:.5f}")
        else:
            print("No price found where the market clears.")

        # Saves the results in a dictionary, appending 
        iteration_3_results = {
            "Optimal Price for Consumer A": f"{price:.5f}"
        }
   
        # Append the results to the list "results" which we defined in the very start
        self.results.append(iteration_3_results)

        # Return the results dictionary in order to call the class in the jupiter notebook
        return iteration_3_results