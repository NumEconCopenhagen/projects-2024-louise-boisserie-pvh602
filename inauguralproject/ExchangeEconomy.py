from types import SimpleNamespace
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize


class ExchangeEconomyClass2:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

        # c. other parameters
        par.N = 75
        par.p2 = 1

    def utility_A(self,x1A,x2A):
        par = self.par

        # returns utility function of A :
        return x1A** par.alpha*x2A**(1-par.alpha) 
    
    def utility_wA(self):
        par = self.par

        # returns utility function of A with endowments instead :
        return par.w1A** par.alpha*par.w2A**(1-par.alpha) 
    
    def utility_B(self,x1B,x2B):
        par = self.par

        # returns utility function of B :
        return x1B** par.beta*x2B**(1-par.beta)
    
    def utility_wB(self):
        par = self.par

        # returns utility function of B with endowments instead :
        return (1-par.w1A)** par.beta*(1-par.w2A)**(1-par.beta) 
    
    def grid(self):
        par = self.par
        N = par.N

        # set all values x can take :
        x_values = np.linspace(0, 1, N+1)

        # returns two arrays, one for each good :
        return np.meshgrid(x_values, x_values)

    def plot_utilities(self, ax_A):
        par = self.par

        # create arrays of values for A from the grid function :        
        x1A_values, x2A_values = self.grid() 

        # save utility values from goods and from endowments :
        utility_A_values = self.utility_A(x1A_values, x2A_values)
        utility_wA_values = self.utility_wA()

        # implement the first conditon :
        feasible_A_combinations = utility_A_values >= utility_wA_values

        # create values for B from A's values :
        x1B_values = 1 - x1A_values
        x2B_values = 1 - x2A_values

        # save utility values from goods and from endowments :
        utility_B_values = self.utility_B(x1B_values, x2B_values)
        utility_wB_value = self.utility_wB()

        # implement the first conditon :
        feasible_B_combinations = utility_B_values >= utility_wB_value

        # create plot with all feasible combinations from A and B :
        ax_A.plot(x1A_values[feasible_B_combinations], x2A_values[feasible_B_combinations], color='red', label='Combinations of B')
        ax_A.plot(x1A_values[feasible_A_combinations], x2A_values[feasible_A_combinations], color='blue', label='Combinations of A')
        ax_A.legend(frameon=True, loc='upper right', bbox_to_anchor=(1.6, 1.0))


    def demand_A(self,p1):
        par = self.par 

        # compute each good for A : 
        x1A = par.alpha*(p1*par.w1A + par.p2*par.w2A)/p1
        x2A = (1-par.alpha)*(p1*par.w1A + par.p2*par.w2A)/par.p2
        return x1A,x2A

    def demand_B(self,p1):
        par = self.par

        # compute each good for B :
        x1B = par.beta*(p1*(1-par.w1A) + par.p2*(1-par.w2A))/p1
        x2B = (1-par.beta)*(p1*(1-par.w1A) + par.p2*(1-par.w2A))/par.p2
        return x1B,x2B

    def check_market_clearing(self,p1):
        par = self.par

        # call each method to unpack solutions :
        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        # compute each epsilon : 
        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)
        return eps1, eps2
    
    def objective(self, p1):
        par = self.par

        # call demand B's function to unpack solutions :
        x1B,x2B = self.demand_B(p1)

        # compute A's utility from B's optimal consumption :
        utility = self.utility_A(1 - x1B, 1 - x2B)
        return -utility  
    
    def find_allocation(self,p1):
        par = self.par

        # maximize the objective function (because minus in front of utlity):
        result = minimize_scalar(self.objective, bounds=(0.5, 2.5), method='bounded')

        # unpack solutions : 
        p1_optimal = result.x
        x1B_optimal,x2B_optimal = self.demand_B(p1_optimal)

        # compute A's optimal consumption :
        x1A_optimal = 1 - x1B_optimal
        x2A_optimal = 1 - x2B_optimal
        return p1_optimal, x1A_optimal, x2A_optimal, x1B_optimal, x2B_optimal
    
    def find_allocation_in_C(self):
        par = self.par 

        def objective_A(xA):
            x1A,x2A = xA 
            return - self.utility_A(x1A,x2A)
        
        def constraint_A2(xA):
            x1A,x2A = xA 
            x1B = 1 - x1A
            x2B = 1 - x2A 
            return [x1A + x1B - 1, x2A + x2B - 1]
        
        xA_guess = [0.5,0.5]
        bounds = [(0,1),(0,1)]
        cons = {'type': 'ineq', 'fun': constraint_A2}
        result = minimize(objective_A, xA_guess, bounds=bounds, constraints=cons)

        # the optimal allocation
        x1A_optimal, x2A_optimal = result.x
        x1B_optimal = 1 - x1A_optimal
        x2B_optimal = 1 - x2A_optimal

        # Compute prices such that B's optimal consumption equals A's optimal consumption
        p1_optimal = (par.alpha * par.w1A + (1 - par.alpha) * (1 - par.w1A)) / x1A_optimal
        return p1_optimal, x1A_optimal, x2A_optimal, x1B_optimal, x2B_optimal

    def find_allocation_no_restrictions(self):
        par = self.par 

        def objective_A(xA):
            x1A,x2A = xA 
            return - self.utility_A(x1A,x2A)
        
        xA_guess = [0.5,0.5]
        bounds = [(0,1),(0,1)]
        result = minimize(objective_A, xA_guess, bounds=bounds)

        # the optimal allocation
        x1A_optimal, x2A_optimal = result.x
        x1B_optimal = 1 - x1A_optimal
        x2B_optimal = 1 - x2A_optimal

        # compute prices so that B's optimal consumption is equal to A's optimal consumption
        p1_optimal = (par.alpha * par.w1A + (1 - par.alpha) * (1 - par.w1A)) / x1A_optimal
        return p1_optimal, x1A_optimal, x2A_optimal, x1B_optimal, x2B_optimal


    def joint_utility(self, x):
        par = self.par
        xA1, xA2 = x[0], x[1]
        xB1, xB2 = 1 - xA1, 1 - xA2
        return -self.utility_A(xA1, xA2) - self.utility_B(xB1, xB2)

    def find_resulting_allocation(self):
        par = self.par
        bounds = [(0, 1), (0, 1)]
        x_guess = [0.5, 0.5]        
        result = minimize(self.joint_utility, x_guess, bounds=bounds)
        xA_optimal = result.x
        return xA_optimal

    def find_equilibrium_allocation(self, omegaA):
        self.par.p2 = 1
        self.par.w1A, self.par.w2A = omegaA
        p1_initial_guess = 1.0 
        result = minimize(lambda p1: np.sum(np.abs(self.check_market_clearing(p1))), p1_initial_guess, method='Nelder-Mead')
        p1_optimal = result.x[0]
        x1A_optimal, x2A_optimal = self.demand_A(p1_optimal)
        x1B_optimal, x2B_optimal = self.demand_B(p1_optimal)
        return x1A_optimal, x2A_optimal, x1B_optimal, x2B_optimal



