from modules.base_modules import AllConv
from bidir.utils import assertEqual
import torch
from torch import Tensor
import torch.nn as nn
import torch.nn.functional as F


class DeepSetNet(nn.Module):
    def __init__(self, element_dim, set_dim, hidden_dim=None):
        super().__init__()
        self.element_dim = element_dim
        self.set_dim = set_dim
        if not hidden_dim:
            hidden_dim = set_dim
        self.hidden_dim = hidden_dim

        self.lin1 = nn.Linear(element_dim, hidden_dim)
        self.lin2 = nn.Linear(hidden_dim, set_dim)

    def forward(self, node_embeddings: Tensor):
        N = node_embeddings.shape[0]
        assertEqual(node_embeddings.shape[1], self.element_dim)
        out = F.relu(self.lin1(node_embeddings))
        assertEqual(out.shape, (N, self.hidden_dim))
        out = torch.sum(out, dim=0)
        assertEqual(out.shape, (self.hidden_dim, ))
        out = self.lin2(out)
        assertEqual(out.shape, (self.set_dim, ))
        return out


class PointerNet(nn.Module):
    def __init__(self, input_dim, query_dim, hidden_dim=64):
        super().__init__()
        self.input_dim = input_dim
        self.query_dim = query_dim
        self.hidden_dim = hidden_dim
        self.W1 = nn.Linear(self.input_dim, self.hidden_dim)
        self.W2 = nn.Linear(self.query_dim, self.hidden_dim)
        self.V = nn.Linear(self.hidden_dim, 1)

    def forward(self, inputs, queries):
        """
        Input:
            inputs: tensor of shape (N, input_dim)
            queries: tensor of shape (query_dim,)

        Output:
            tensor of shape (N,) with unnormalized probability of choosing each
            input.

        Computes additive attention identically to the pointer net paper:
        https://arxiv.org/pdf/1506.03134.pdf
        """
        N = inputs.shape[0]
        assertEqual(inputs.shape, (N, self.input_dim))
        assertEqual(queries.shape, (self.query_dim, ))

        w1_out = self.W1(inputs)
        assertEqual(w1_out.shape, (N, self.hidden_dim))
        w2_out = self.W2(queries)
        assertEqual(w2_out.shape, (self.hidden_dim, ))
        w2_repeated = w2_out.repeat(N, 1)
        assertEqual(w2_repeated.shape, (N, self.hidden_dim))
        u = self.V(torch.tanh(w2_out + w2_repeated))
        assertEqual(u.shape, (N, 1))
        u = u.squeeze(1)
        assertEqual(u.shape, (N, ))
        return u


class CNN(nn.Module):
    def __init__(self, in_channels=10, output_dim=64):
        super().__init__()

        self.all_conv = AllConv(residual_blocks=2,
                                input_filters=in_channels,
                                residual_filters=32,
                                conv_1x1s=2,
                                output_dim=output_dim,
                                conv_1x1_filters=64,
                                pooling='max')

    def forward(self, x):
        """
        Input: tensor of shape (batch, channels, height, width)
        Output: tensor of shape (batch, output_dim)
        """

        # (B, C, H, W) to (B, output_dim)
        x = x.to(torch.float32)
        x = self.all_conv(x)

        # test if this is actually helping.
        # return torch.rand(x.shape)
        return x


class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, output_dim=64):
        super().__init__()
        # see pytorch documentation for more details
        self.lstm = nn.LSTM(input_size=input_dim,
                            hidden_size=hidden_dim,
                            num_layers=1,
                            batch_first=True,
                            bidirectional=False)

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        """
        Input: tensor of shape
            (batch, seq_len, input_dim)
        Output: tensor of shape
            (batch_size, output_dim)
        """

        batch = x.shape[0]
        x = x.to(torch.float32)

        # (batch, seq_len, input_dim) to (batch, seq_len, hidden_dim)
        out, (last_hidden, _) = self.lstm(x)

        assert last_hidden.shape == (batch, 1, self.hidden_dim)

        last_hidden = torch.squeeze(last_hidden, 1)

        assert last_hidden.shape == (batch, self.hidden_dim)

        # TODO: nonlinearity?
        out = self.fc(last_hidden)
        assert out.shape == (batch, self.output_dim)

        return out
