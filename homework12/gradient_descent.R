# Gradient Descent Algorithm
gradientDescent <- function(X, y, alpha = 0.05, iterations = 1000) {
  X <- cbind(1, as.matrix(X))   # for convention
  m <- length(y)                # number of training examples
  theta <- matrix(rep(0, ncol(X)), nrow = ncol(X)) # parameters
  
  theta_history <- list()  # parameters
  cost_history  <- c()     # cost function values
  
  for (i in 1:iterations) {
    # Update parameters theta
    theta <- theta - alpha * (1 / m) * (t(X) %*% (X %*% theta - y))
    
    # Save previous values of cost function and parameters theta
    theta_history[[i]] <- theta
    cost_history[i]    <- sum((X %*% theta - y)^2) / (2 * m)
  }
  
  list(theta = theta, 
       theta_history = theta_history, 
       cost_history = cost_history)
}
