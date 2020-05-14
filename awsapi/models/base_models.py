import torch
import torch.nn as nn

def get_block_layer(c_in, c_out, kernel_size=3, padding=1):
    return nn.Sequential(nn.BatchNorm2d(c_in), 
                         nn.ReLU(), 
                         nn.Conv2d(c_in, c_out, kernel_size, padding=padding))
    

class NeuralTransform(nn.Module):
    def __init__(self, c_in, c_out, num_layers, gr):
        super().__init__()
        self.c_in = c_in
        self.c_out = c_out
        
        self.layers = nn.ModuleList()
        
        c_prev = c_in
        for layer_idx in range(num_layers-1):
            self.layers.append(get_block_layer(c_prev, gr))
            c_prev += gr
            
        self.final_layer = get_block_layer(c_prev, c_out)
        
        
    def forward(self, x):
        for layer in self.layers:
            x = torch.cat((x, layer(x)), axis=1)
        x = self.final_layer(x)
        return x
    
def get_down_sample_layer(c, kernel_size=(2,2), stride=(2,2)):
    return nn.Conv2d(c, c, kernel_size=kernel_size, stride=stride)
def get_up_sample_layer(c, kernel_size=(2,2), stride=(2,2)):
    return nn.ConvTranspose2d(c, c, kernel_size=kernel_size, stride=stride)

# frequency time convolutional neural network for generator
class FTCNNGenerator(nn.Module):
    def __init__(self, c_in, cs, c_out=None, num_layers_per_block=4, block_gr=24):
        super().__init__()
        
        if c_out is None:
            c_out = c_in
        
        rcs = list(reversed(cs))
        
        self.conv_first = nn.Conv2d(c_in, cs[0], kernel_size=1)
        self.conv_last = nn.Conv2d(rcs[-1], c_out, kernel_size=1)
        
        self.left = nn.ModuleList([NeuralTransform(c_in, c_out, num_layers_per_block, block_gr) for c_in, c_out in zip(cs, cs[1:])])
        self.right = nn.ModuleList([NeuralTransform(2*c_in, c_out, num_layers_per_block, block_gr) for c_in, c_out in zip(rcs, rcs[1:])])
        
        self.midnt = NeuralTransform(cs[-1], cs[-1], num_layers_per_block, block_gr)
        
        self.downs = nn.ModuleList([get_down_sample_layer(c) for c in cs[1:]])
        self.ups = nn.ModuleList([get_up_sample_layer(c) for c in rcs[:-1]])
    
    def forward(self, x):
        x = self.conv_first(x)
        
        residuals = []
        shapes = []
        for nt, down in zip(self.left, self.downs):
            x = nt(x)
            residuals.insert(0, x)
            shapes.insert(0, x.shape)
            x = down(x)
        
        x = self.midnt(x)
        
        for nt, up, residual, shape in zip(self.right, self.ups, residuals, shapes):
            x = up(x, output_size=shape)
            x = torch.cat((x, residual), dim=1)
            x = nt(x)
        
        x = self.conv_last(x)
        return x
    
    
    
# frequency time convolutional neural network for discriminator
class FTCNNDiscrimminator(nn.Module):
    def __init__(self, c_in, cs, input_hw, fcs=[100, 10, 10, 1], num_layers_per_block=4, block_gr=24):
        super().__init__()
        
        self.conv_first = nn.Conv2d(c_in, cs[0], kernel_size=1)
        
        self.nts = nn.ModuleList([NeuralTransform(c_in, c_out, num_layers_per_block, block_gr) for c_in, c_out in zip(cs, cs[1:])])
        self.dss = nn.ModuleList([get_down_sample_layer(c_out) for c_out in cs[1:]])
        
        h = input_hw[0] // (2**len(self.dss))
        w = input_hw[1] // (2**len(self.dss))
    
        self.fc1d1 = cs[-1]*h*w
            
        fcs.insert(0, self.fc1d1)
        self.fcs = nn.ModuleList([nn.Linear(d1, d2) for d1, d2 in zip(fcs, fcs[1:])])
    
    def forward(self, x):
        x = self.conv_first(x)
        
        for nt, down in zip(self.nts, self.dss):
            x = nt(x)
            x = down(x)
        x = x.view(-1, self.fc1d1)
        
        for fc in self.fcs[:-1]:
            x = fc(x)
            x = torch.relu(x)
        
        x = self.fcs[-1](x)
        x = torch.sigmoid(x)
        return x[:, 0]
