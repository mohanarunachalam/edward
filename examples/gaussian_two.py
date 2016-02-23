#!/usr/bin/env python
"""
Probability model
    Posterior: (2-dimensional) Gaussian
Variational model
    Likelihood: Mean-field Gaussian
"""
import tensorflow as tf
import blackbox as bb

from blackbox.stats import gaussian_log_prob
from blackbox.util import get_dims

class Gaussian:
    """
    p(x, z) = p(z) = p(z | x) = Gaussian(z; mu, Sigma)
    """
    def __init__(self, mu, Sigma):
        self.mu = mu
        self.Sigma = Sigma
        self.num_vars = get_dims(mu)[0]

    def log_prob(self, zs):
        return tf.pack([gaussian_log_prob(z, mu, Sigma)
                        for z in tf.unpack(zs)])

bb.set_seed(42)
mu = tf.constant([1.0, 1.0])
Sigma = tf.constant(
[[1.0, 0.1],
 [0.1, 1.0]])
model = Gaussian(mu, Sigma)
variational = bb.MFGaussian(model.num_vars)

inference = bb.MFVI(model, variational)
inference.run(n_iter=10000)
