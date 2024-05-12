import numpy as np

def solve_backwards(beta,W,T):
    # Initializing
    Vstar = np.nan+np.zeros((W+1,T))
    Cstar = np.nan + np.zeros((W+1,T))
    Cstar[:,T-1] = np.arange(W+1) 
    Vstar[:,T-1] = np.sqrt(Cstar[:,T-1])
    C_backwards = np.empty(T)

    # Solving
    for t in range(T-2, -1, -1):  
        for w in range(W+1):
            c = np.arange(w+1)
            w_c = w - c
            V_next = Vstar[w_c,t+1]
            V_guess = np.sqrt(c)+beta*V_next
            Vstar[w,t] = np.amax(V_guess)
            Cstar[w,t] = np.argmax(V_guess)
    
    # Simulating 
    W_now = W
    for t in range(T):
        W_now = int(W_now)  
        C_backwards[t] = Cstar[W_now,t]  
        W_now = W_now-C_backwards[t] 
    
    return C_backwards

def solve_VFI(W, beta, max_iter=500, tol=1e-3):
    grid_W = np.arange(W + 1)
    Cstar = np.zeros(W + 1)
    V_now = np.zeros(W + 1)
    it = 0
    delta = tol + 1
    
    while (it <= max_iter and delta > tol):
        it = it + 1
        V_next = V_now.copy()
        for w in range(W + 1):
            c = np.arange(w + 1)
            w_next = w - c
            V_guess = np.sqrt(c) + beta * V_next[w_next]
            V_now[w] = np.amax(V_guess)
            Cstar[w] = np.argmax(V_guess)
        delta = np.amax(np.abs(V_now - V_next))
    
    return Cstar