import argparse
#import pprint

def read_data(file_name):
    '''
    Reads integer numbers from a text file and returns them in a list
    '''
    X = []
    with open(file_name) as f:
        for line in f:
            X.extend([int (num) for num in line.split()])
    return X
        

def lance_williams(X, method):
    '''
    Implements the Lance-Williams algorithm for calculating the distance 
    between clusters.
    
    Parameters:
    - X : sorted list of integers
    - method: string indicating the method to use for merging clusters:
        "single", "complete", "average", or "ward"
    
    Returns:
    - Z: list of tuples of length 4, where n is the number of objects
        The i-th tuple contains information about the i-th merge:
        - Z[i][0]: first cluster merged
        - Z[i][1]: second cluster merged
        - Z[i][2]: distance between the two merged clusters
        - Z[i][3]: size of the new cluster
    '''
    n0 = len(X)
    # Compute initial pairwise distances
    # D: list of lists of pairwise distances between objects
    D = [ [0.0] * n0 for _ in range(n0)]
    for i in range(n0):
        for j in range(i+1, n0):  # distance is symmetric 
            D[i][j] = D[j][i] = float(abs(X[i] - X[j]))


    Z = []
    # Initialize each object as its own cluster
    clusters = [ (X[i],) for i in range(n0)]
    n = n0
    # Iterate until all objects are in a single cluster
    for k in range(n0-1):        
        # Find closest pair of clusters
        s,t = min(((i, j) for i in range(n) for j in range(i+1, n)), key=lambda x: D[x[0]][x[1]])
        d_min = D[s][t]        
        u = s
        if method == "single":
            for v in range(n):
                if v!=s and v!=t:                    
                    tmp = 0.5 * D[s][v] + 0.5 * D[t][v] - 0.5 * abs(D[s][v]-D[t][v])
                    D[u][v] = D[v][u] = tmp

        elif method == "complete":
            for v in range(n):
                if v!=s and v!=t:                    
                    tmp = 0.5 * D[s][v] + 0.5 * D[t][v] + 0.5 * abs(D[u][v]-D[t][v])
                    D[u][v] = D[v][u] = tmp
        elif method == "average":
            w_s,w_t = len(clusters[s]),len(clusters[t])
            w_st = w_s + w_t
            for v in range(n):
                if v!=s and v!=t:
                    D[u][v] = D[v][u] = w_s/w_st * D[s][v] + w_t / w_st*D[t][v]
        elif method=="ward":
            w_s,w_t = len(clusters[s]),len(clusters[t])
            w_st = w_s + w_t            
            for v in range(n):
                if v!=s and v!=t:
                    w_v   = len(clusters[v])
                    w_stv = w_st + w_v
                    D[u][v] = D[v][u] = (w_s+w_v)/w_stv * D[s][v] + (w_t+w_v) / w_stv * D[t][v] -w_v/w_stv*d_min

        # Store the requested information about the merge
        Z.append((clusters[s], clusters[t], d_min, len(clusters[s])+len(clusters[t])))        
        new_cluster = clusters[s] + clusters[t]
        #print(f'merge {clusters[s]},{clusters[t]} with dist {d_min:.2f} gives {new_cluster}')
        clusters.pop(t)
        clusters[s] = new_cluster   

        # Remove the distance between the merged clusters from the distance matrix
        for row in D:
            row.pop(t)
        D.pop(t)
        n = n - 1
    return Z


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hierarchical Clustering')
    parser.add_argument('method', type=str)
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    #X = [7, 10, 4, 20, 2, 25, 19, 6, 12, 1]        
    X = read_data(args.input_filename)
    X.sort()
    #print(X)
    Z = lance_williams(X, args.method)    
    
    for t in Z:
        s1 = str(t[0]).replace(',', '')
        s2 = str(t[1]).replace(',', '')
        print(f'{s1} {s2} {t[2]:.2f} {t[3]}')
        