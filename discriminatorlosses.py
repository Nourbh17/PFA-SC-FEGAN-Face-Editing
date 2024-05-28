# -*- coding: utf-8 -*-
"""DiscriminatorLosses.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AfxdQJBtBwsR4giFy5OpBy24Dzh4KL4l
"""

import tensorflow as tf

class DiscrimnatorLosses():
    #The primary purpose of this loss function is to ensure that the discriminator (or critic) network maintains gradients with a norm of approximately 1, which helps enforce
    #the Lipschitz constraint necessary for WGANs. This helps improve the stability of the GAN training process.
    def GPLoss(model, ground_truth, complete_image, mask):
        batch, w, h, c = ground_truth.get_shape().as_list()
        alpha = tf.random.normal([batch, 1, 1, 1], 0.0, 1.0)
        diff = complete_image - ground_truth
        interpolated = (complete_image + alpha * diff) * mask

        with tf.GradientTape() as gp_tape:
            gp_tape.watch(interpolated)  #watch explicitly tells the GradientTape to track gradients with respect to a specific tensor.
            #Usage: It's used when the tensor you're interested in computing gradients for is not created by operations within the GradientTape context
            pred = model(interpolated, training=True)
        grads = gp_tape.gradient(pred, [interpolated])[0]
        norm = tf.sqrt(tf.reduce_sum(tf.square(grads)))
        gp = tf.reduce_mean((norm - 1.0) ** 2)
        return gp

    def total_dis_loss(dis_real,dis_fake,model,ground_truth,complete_image,mask):
      hinge_pos= tf.reduce_mean(1 - dis_real)
      hinge_neg = tf.reduce_mean(1 + dis_fake)
      dis_loss =  tf.add(hinge_pos,hinge_neg)
      loss=dis_loss+10.*GPLoss(model,ground_truth,complete_image,mask)
      return loss