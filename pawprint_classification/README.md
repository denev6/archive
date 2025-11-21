# PawPrint Classification

Dataset: [PawPrint-Project](https://songinpyo.github.io/PawPrint-Project/)

```bib
@misc{song2025pawprintfootprintstheseidentifying,
  title={PawPrint: Whose Footprints Are These? Identifying Animal Individuals by Their Footprints}, 
  author={Inpyo Song and Hyemin Hwang and Jangwon Lee},
  year={2025},
  eprint={2505.17445},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2505.17445}, 
}
```

## What I learned

### Pre-trained weights

> Do Better ImageNet Models Transfer Better (CVPR, 2019)

- Transfer learning with pre-trained ImageNet weights can accelerate model convergence.
- PyTorch provides most major model architectures (e.g., ResNet, EfficientNet, ViT) pre-trained on ImageNet

```python
class ResNet(nn.Module):
    def __init__(self, num_labels):
        super(ResNet, self).__init__()
        # Pre-trained ResNet
        self.feature_extractor = models.resnet152(weights=models.ResNet152_Weights.IMAGENET1K_V1)
        # Initialize Linear Layer        
        n_features = self.feature_extractor.fc.in_features
        self.feature_extractor.fc = nn.Identity()
        self.classifier = nn.Linear(n_features, num_labels)

    def forward(self, x):
        features = self.feature_extractor(x)
        output = self.classifier(features)
        return output
```

### Inductive Bias

Due to their inherent inductive biases, CNNs often outperform Transformers when training data is limited.

### Data augmentation

> RandAugment: Practical automated data augmentation with a reduced search space (CVPR, 2020)
>
> TrivialAugment: Tuning-free Yet State-of-the-Art Data Augmentation (CVPR, 2021)

- According to both papers, simple random augmentations can boost classification performance.
- Implementation is straightforward in PyTorch, requiring only a few extra lines of code.

```python
# RandAugment
transforms.Compose([
    transforms.RandAugment(),
    transforms.ToTensor(),
])

# TrivialAugment
transforms.Compose([
    transforms.TrivialAugmentWide(),
    transforms.ToTensor(),
])

# Custom
augmentation_pipeline = [
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomApply(
        [
            transforms.ColorJitter(
                brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1
            ),
            transforms.GaussianBlur(kernel_size=5, sigma=1.0),
        ],
        p=0.5,
    ),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
]
```

### LR Scheduler

> SGDR: Stochastic Gradient Descent with Warm Restarts (ICLR, 2017)
> 
> Super-Convergence: Very Fast Training of Neural Networks Using Large Learning Rates (SPIE, 2019)
> 
> Adam: A Method for Stochastic Optimization (2014)

- When using SGD, a learning rate (LR) scheduler can help achieve faster convergence.
- PyTorch offers several effective schedulers.
- Theoretically, schedulers have a minimal effect on Adam-family optimizers (like Adam or AdamW) because they already incorporate an adaptive learning rate mechanism. However, many recent SOTA papers train their models using AdamW with a scheduler, and the prevailing view is that there's no harm in using them together (which is a view I share).

```python
# When the learning rate needs to gradually decrease.
optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100, eta_min=1e-6)
# When you want to apply an initial warmup period.
optim.lr_scheduler.OneCycleLR(optimizer, max_lr=100)
# When warm restarts are necessary.
optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=20)
```

### Mixed Precision

> Mixed Precision Training (ICLR, 2018)

This is a technique known as Mixed Precision, which significantly improves training efficiency by using a combination of 16-bit and 32-bit floating-point precision, rather than the default 32-bit. This is done without sacrificing the model's final performance.

```python
with autocast(
      device_type="cuda", enabled=True, dtype=torch.float16
  ):
      output = model(image_input)
      batch_loss = criterion(output, label)
```
