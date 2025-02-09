import torchvision
import torch.nn as nn
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models.resnet import BasicBlock


def fasterRCNN_resnet18(num_classes):
    # Load the pretrained ResNet18 backbone.
    conv1 = torchvision.models.resnet18(weights=None).conv1
    bn1 = torchvision.models.resnet18(weights=None).bn1
    resnet18_relu = torchvision.models.resnet18(weights=None).relu
    resnet18_max_pool = torchvision.models.resnet18(weights=None).maxpool
    layer1 = torchvision.models.resnet18(weights=None).layer1
    layer2 = torchvision.models.resnet18(weights=None).layer2
    layer3 = torchvision.models.resnet18(weights=None).layer3
    layer4 = torchvision.models.resnet18(weights=None).layer4

    # Add layer extra basicblock
    layer1.add_module('extra', BasicBlock(64, 64))
    layer2.add_module('extra', BasicBlock(128, 128))
    layer3.add_module('extra', BasicBlock(256, 256))
    layer4.add_module('extra', BasicBlock(512, 512))

    backbone = nn.Sequential(
        conv1, bn1, resnet18_relu, resnet18_max_pool, 
        layer1, layer2, layer3, layer4)

    # We need the output channels of the last convolutional layers from
    # the features for the Faster RCNN model.
    # It is 512 for ResNet18.
    backbone.out_channels = 512

    # Generate anchors using the RPN. Here, we are using 5x3 anchors.
    # Meaning, anchors with 5 different sizes and 3 different aspect 
    # ratios.
    anchor_generator = AnchorGenerator(
        sizes=((32, 64, 128, 256, 512),),
        aspect_ratios=((0.5, 1.0, 2.0),)
    )

    # Feature maps to perform RoI cropping.
    # If backbone returns a Tensor, `featmap_names` is expected to
    # be [0]. We can choose which feature maps to use.
    roi_pooler = torchvision.ops.MultiScaleRoIAlign(
        featmap_names=['0'],
        output_size=7,
        sampling_ratio=2
    )

    # Final Faster RCNN model.
    model = FasterRCNN(
        backbone=backbone,
        num_classes=num_classes,
        rpn_anchor_generator=anchor_generator,
        box_roi_pool=roi_pooler
    )
    return model