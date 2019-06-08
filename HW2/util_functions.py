import numpy as np


def softmax(x):

    if len(x.shape) == 1:
        z = x - np.max(x)
        exp_z = np.exp(z)
        exp_sum = np.sum(exp_z)

    else:
        z = x - np.max(x, axis=1)[:, np.newaxis]
        exp_z = np.exp(z)
        exp_sum = np.sum(exp_z, axis=1)[:, np.newaxis]

    return exp_z / exp_sum


def relu(x):
    return np.maximum(x, 0)


def relu_derivative(x):
    return relu(x) / np.abs(x + 1e-5)


def sigmoid(x):
    z = np.where(x >= 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))
    return z


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


def conv2d(input_, weights, biases, stride=1):
    """ Implements a 2-D convolution operation.
    Will perform using matrix multiplication operations
    Arguments:
    inputs -- an input signal with the dimensions of N X C X H X W
         N is the batch size, C is number of channels, and H and W
         are the input height and width
    weights -- the kernel to perform convolution with. has a dimension of D x h X w
        where D is number of filters to apply, h and w are the kernel dimensions
    biases - bias terms. always 1 dimension array of shape D
    """

    N, C, H, W = input_.shape
    D, _, h, w = weights.shape
    w_out = (H - h) // stride + 1
    h_out = (W - w) // stride + 1

    input_cols = _im2col(input_, weights, stride)
    weight_rows = weights.reshape(D, C * h * w)
    biases = biases.reshape(D, 1)  # in order to enable broadcasting

    conv_res = weight_rows @ input_cols + biases
    conv_res_shaped = conv_res.reshape(N, D, h_out, w_out)

    return conv_res_shaped


def _im2col(input_, weights, stride):

    _, C, H, W = input_.shape
    D, _, w, h = weights.shape
    w_out = (H - h) // stride + 1
    h_out = (W - w) // stride + 1

    i0 = np.repeat(np.arange(h), w)
    i0 = np.tile(i0, C)
    i1 = stride * np.repeat(np.arange(h_out), w_out)

    j0 = np.tile(np.arange(w), h * C)
    j1 = stride * np.tile(np.arange(w_out), h_out)

    i = i0.reshape(-1, 1) + i1.reshape(1, -1)
    j = j0.reshape(-1, 1) + j1.reshape(1, -1)
    k = np.repeat(np.arange(C), h * w).reshape(-1, 1)

    input_cols = input_[:, k, i, j]
    return input_cols


