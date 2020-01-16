import logging
import torch
import numpy as np
from torch import nn


log = logging.getLogger('cnn')
log.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)

class Bottleneck(nn.Module):
	expansion = 4
	def __init__(self, in_channel, n_filters, downsample=None, stride=1):
		super(Bottleneck, self).__init__()
		# first 1x1
		self.cv1 = nn.Conv2d(in_channel, n_filters, kernel_size=1)
		self.bn1 = nn.BatchNorm2d(n_filters)

		# second 3x3
		# FIXME: padding=1 and stride=2 should be controlled
		self.cv2 = nn.Conv2d(n_filters, n_filters, kernel_size=3, padding=1, stride=stride)
		self.bn2 = nn.BatchNorm2d(n_filters)

		# third 1x1
		self.cv3 = nn.Conv2d(n_filters, n_filters*self.expansion, kernel_size=1)
		self.bn3 = nn.BatchNorm2d(n_filters*self.expansion)
		self.relu = nn.ReLU()

		# downsample
		self.downsample = downsample

	def forward(self, x):
		identity = x
		out = self.cv1(x)
		out = self.bn1(out)
		log.debug('cv1 result: {}'.format(out.shape))

		out = self.cv2(out)
		out = self.bn2(out)
		log.debug('cv2 result: {}'.format(out.shape))

		out = self.cv3(out)
		out = self.bn3(out)
		out = self.relu(out)
		log.debug('cv3 result: {}'.format(out.shape))

		# do something about downsample here
		if self.downsample is not None:
			identity = self.downsample(x)

		out += identity
		out = self.relu(out)

		log.debug('out: {}'.format(out.shape))
		log.debug('identity: {}'.format(identity.shape))
		return out


def get_padding(i):
	return int(np.ceil(i/2) - 1)

class Resnet(nn.Module):
	def __init__(self, bottleneck, layers, num_classes=1000, zero_init_residual=False, in_channel=3):
		super(Resnet, self).__init__()
	
		self.planes = 64
		k = 7
		n_pad = get_padding(k)
		self.cv1 = nn.Conv2d(in_channel, self.planes, kernel_size=k, padding=n_pad, stride=2, bias=False)
		self.bn1 = nn.BatchNorm2d(self.planes)
		self.relu = nn.ReLU()
		self.mx1 = nn.MaxPool2d(kernel_size=3, stride=2, padding=get_padding(3))

		# add bottleneck layer
		self.layer1 = self._add_bottleneck_layer(bottleneck, 64, layers[0])
		self.layer2 = self._add_bottleneck_layer(bottleneck, 128, layers[1], stride=2)
		self.layer3 = self._add_bottleneck_layer(bottleneck, 256, layers[2], stride=2)
		self.layer4 = self._add_bottleneck_layer(bottleneck, 512, layers[3], stride=2)

		# average pooling and fully-connected layer
		self.avgpool = nn.AdaptiveAvgPool2d((1,1))
		self.fc = nn.Linear(512*bottleneck.expansion, num_classes)
		
		# zero-initialize the residual block
		if zero_init_residual:
			for m in self.modules():
				if isinstance(m, Bottleneck):
					nn.init.constant_(m.bn3.weight, 0)

	def _add_bottleneck_layer(self, block, out_planes, n_block, stride=1):
		downsample = None
		if stride != 1 or self.planes != out_planes*block.expansion:
			# do downsampling
			downsample = nn.Sequential(*[
				nn.Conv2d(self.planes, out_planes*block.expansion, kernel_size=1, stride=stride),
				nn.BatchNorm2d(out_planes*block.expansion)
			])
			log.debug('downsample {}'.format(downsample))

		layers = []
		layers.append(block(self.planes, out_planes, downsample=downsample, stride=stride))
		self.planes = out_planes*block.expansion
		for _ in range(1, n_block):
			layers.append(block(self.planes, out_planes))
		return nn.Sequential(*layers)

	def forward(self, x):
		out = self.cv1(x)
		out = self.bn1(out)
		out = self.relu(out)
		out = self.mx1(out)
		log.info('first basic convolution layer has been added')

		out = self.layer1(out)
		out = self.layer2(out)
		out = self.layer3(out)
		out = self.layer4(out)
		log.info('all bottleneck layers has been added')

		# for classifier
		out = self.avgpool(out)
		out = self.fc(out.reshape(out.shape[0], -1))
		log.info('fully-connected layer has been added')

		return out


bs = 5
images = np.random.random((bs, 3, 300, 200))
images = torch.Tensor(images)
bottleneck = Bottleneck
model = Resnet(bottleneck, [3,4,5,3], num_classes=10)
pred = model(images)
print(pred.shape)




