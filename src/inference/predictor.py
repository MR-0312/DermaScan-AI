"""
=================================================================
PREDICTOR — Single Image Inference Pipeline
=================================================================
"""
import pathlib
pathlib.PosixPath = pathlib.WindowsPath


import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from typing import Dict, Tuple
import json


class SkinPredictor:
    """
    Production inference pipeline.
    Loads model once, predicts on any image.
    """
    
    def __init__(
        self,
        model_path: str = "checkpoints/best_model.pth",
        class_config_path: str = "configs/class_config.json",
        device: str = None,
        img_size: int = 224,
    ):
        # Device
        if device:
            self.device = torch.device(device)
        elif torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
        
        # Load class config
        with open(class_config_path, 'r') as f:
            self.class_config = json.load(f)
        
        self.num_classes = len(self.class_config)
        self.class_names = [self.class_config[str(i)]['name'] for i in range(self.num_classes)]
        
        # Build model
        self.model = self._build_model()
        self._load_weights(model_path)
        self.model.eval()
        
        # Transform
        self.transform = A.Compose([
            A.Resize(img_size, img_size),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2(),
        ])
        
        print(f"✅ Predictor ready on {self.device}")
    
    def _build_model(self):
        """Build model architecture (must match training)."""
        import timm
        import torch.nn as nn
        
        class DermaScanModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.backbone = timm.create_model(
                    'efficientnet_b3', pretrained=False,
                    num_classes=0, drop_rate=0.0,
                )
                self.feature_dim = self.backbone.num_features
                self.head = nn.Sequential(
                    nn.Linear(self.feature_dim, 512),
                    nn.BatchNorm1d(512),
                    nn.SiLU(inplace=True),
                    nn.Dropout(0.3),
                    nn.Linear(512, 128),
                    nn.BatchNorm1d(128),
                    nn.SiLU(inplace=True),
                    nn.Dropout(0.15),
                    nn.Linear(128, 13),
                )
            
            def forward(self, x):
                return self.head(self.backbone(x))
        
        return DermaScanModel().to(self.device)
    
    def _load_weights(self, model_path: str):
        """Load trained weights."""
        checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
        
        if 'model_state_dict' in checkpoint:
            self.model.load_state_dict(checkpoint['model_state_dict'])
        else:
            self.model.load_state_dict(checkpoint)
        
        print(f"   Weights loaded from {model_path}")
    
    @torch.no_grad()
    def predict(self, image) -> Dict:
        """
        Predict on a single image.
        
        Args:
            image: PIL Image, numpy array, or file path
            
        Returns:
            Dictionary with prediction results
        """
        # Handle different input types
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        elif isinstance(image, Image.Image):
            image = image.convert('RGB')
        
        img_array = np.array(image)
        
        # Transform
        tensor = self.transform(image=img_array)['image'].unsqueeze(0)
        tensor = tensor.to(self.device)
        
        # Predict
        logits = self.model(tensor)
        probabilities = F.softmax(logits, dim=1)[0].cpu().numpy()
        
        predicted_class = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_class])
        
        return {
            "predicted_class": predicted_class,
            "predicted_class_name": self.class_names[predicted_class],
            "confidence": confidence,
            "all_probabilities": probabilities,
        }