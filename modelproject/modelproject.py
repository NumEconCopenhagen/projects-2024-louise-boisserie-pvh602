from scipy import optimize
import numpy as np

def solve_backwards(beta,W,T,W_now):
    # Initialize
    Vstar = np.nan+np.zeros([W+1,T])
    Cstar = np.nan + np.zeros([W+1,T])
    Cstar[:,T-1] = np.arange(W+1) 
    Vstar[:,T-1] = np.sqrt(Cstar[:,T-1])
    C_backwards = np.empty(T)

    # Solve
    # loop over periods
    for t in range(T-2, -1, -1):  
        
        #loop over states
        for w in range(W+1):
            c = np.arange(w+1)
            w_c = w - c
            V_next = Vstar[w_c,t+1]
            V_guess = np.sqrt(c)+beta*V_next
            Vstar[w,t] = np.amax(V_guess)
            Cstar[w,t] = np.argmax(V_guess)
    
    for t in range(T):
        W_now = int(W_now)  
        C_backwards[t] = Cstar[W_now,t]  
        W_now = W_now-C_backwards[t] 
    
    return C_backwards
