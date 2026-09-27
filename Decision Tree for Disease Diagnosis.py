import numpy as np 

def calculate_gini(y):

    m = len(y)
    if m == 0:
        return 0.0
    
    probabilities = [np.sum(y == c) / m for c in np.unique(y)]
    
    gini = 1.0 - sum([p ** 2 for p in probabilities])
    return gini


def find_best_split(X, y):
    best_gain = -1
    best_split_idx, best_split_val = None, None
    current_gini = calculate_gini(y)
    
    n_samples, n_features = X.shape
    
    for feature_idx in range(n_features):
        X_column = X[:, feature_idx]
        thresholds = np.unique(X_column)
        
        for threshold in thresholds:
            
            left_mask = X_column <= threshold
            right_mask = ~left_mask
            
            if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                continue
                
            
            n_l, n_r = np.sum(left_mask), np.sum(right_mask)
            gini_l = calculate_gini(y[left_mask])
            gini_r = calculate_gini(y[right_mask])
            weighted_gini = (n_l / n_samples) * gini_l + (n_r / n_samples) * gini_r
            
            
            gain = current_gini - weighted_gini
            
            if gain > best_gain:
                best_gain = gain
                best_split_idx = feature_idx
                best_split_val = threshold
                
    return best_split_idx, best_split_val