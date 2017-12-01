# Simple implementation of K-Means Algorithm
kMeans <- function(data, K) {
  # For efficiency reasons
  data <- as.matrix(data)
  # Number of features
  m <- nrow(data)
  
  # Randomly initialize K cluster centroids
  centroids <- data[sample(m, K), ]
  
  distance <- c()
  cluster  <- c()
  
  # Run the main k-means algorithm
  repeat {
    # 1. Cluster assignment step
    for (i in 1:m) {
      for (k in 1:K) {
        # Calculate the Euclidean distance
        distance[k] <- sqrt(sum((data[i, ] - centroids[k, ]) ^ 2))
      }
      cluster[i] <- which.min(distance)
    }
    
    # 2. Move centroids step
    centroids_prev <- centroids
    for (k in 1:K) {
      centroids[k, ] <- (1.0 / nrow(data[cluster == k, ])) * 
        colSums(data[cluster == k, ])
    }
    
    # 3. Stop when centroids not moving
    if (identical(centroids, centroids_prev)) {
      break
    }
  }
  
  # Return data about clusterization to caller
  list("cluster"=cluster, "centers"=centroids)
}