"""
=================================================================
RESPONSE ENGINE — The Brain of DermaScan-AI
=================================================================
Takes model prediction → generates complete clinical response:
  - Diagnosis with confidence
  - Severity tier (CANCER / PRE-CANCER / BENIGN / DISEASE)
  - Care advice
  - Hospital recommendation
  - Urgency level
=================================================================
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np


class ResponseEngine:
    """
    Generates structured clinical responses based on model predictions.
    """
    
    def __init__(
        self,
        class_config_path: str = "configs/class_config.json",
        response_templates_path: str = "configs/response_templates.json",
    ):
        # Load class config
        with open(class_config_path, 'r') as f:
            self.class_config = json.load(f)
        
        # Load response templates
        with open(response_templates_path, 'r') as f:
            self.templates = json.load(f)
        
        self.num_classes = len(self.class_config)
        self.class_names = [self.class_config[str(i)]['name'] for i in range(self.num_classes)]
        self.class_tiers = [self.class_config[str(i)]['tier'] for i in range(self.num_classes)]
        
        # Confidence thresholds
        self.HIGH_CONFIDENCE = 0.7
        self.MEDIUM_CONFIDENCE = 0.4
        self.LOW_CONFIDENCE = 0.2
    
    def generate_response(
        self,
        predicted_class: int,
        confidence: float,
        all_probabilities: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Generate a complete response for a prediction.
        
        Args:
            predicted_class: Index of predicted class
            confidence: Confidence of top prediction (0-1)
            all_probabilities: Array of probabilities for all 13 classes
        
        Returns:
            Complete response dictionary
        """
        class_name = self.class_names[predicted_class]
        template = self.templates.get(class_name, {})
        class_info = self.class_config[str(predicted_class)]
        
        # ── Confidence assessment ──
        if confidence >= self.HIGH_CONFIDENCE:
            confidence_level = "HIGH"
            confidence_message = "The AI model has high confidence in this assessment."
        elif confidence >= self.MEDIUM_CONFIDENCE:
            confidence_level = "MEDIUM"
            confidence_message = "The AI model has moderate confidence. Consider getting a professional opinion."
        else:
            confidence_level = "LOW"
            confidence_message = "The AI model has low confidence. This result should be verified by a medical professional."
        
        # ── Check for close second prediction ──
        sorted_indices = np.argsort(all_probabilities)[::-1]
        second_class = sorted_indices[1]
        second_prob = all_probabilities[second_class]
        second_name = self.class_names[second_class]
        
        close_call = (confidence - second_prob) < 0.15
        
        # ── Build differential diagnosis ──
        differential = []
        for idx in sorted_indices[:3]:
            if all_probabilities[idx] > 0.05:
                differential.append({
                    "class_name": self.class_names[idx],
                    "probability": round(float(all_probabilities[idx]), 4),
                    "tier": self.class_tiers[idx],
                })
        
        # ── Is any cancer class in top 3? ──
        cancer_alert = False
        cancer_in_top3 = []
        for d in differential:
            if d['tier'] in ['CANCER', 'PRE-CANCER']:
                cancer_in_top3.append(d)
                if d['probability'] > 0.1:
                    cancer_alert = True
        
        # ── Build response ──
        response = {
            # Core prediction
            "predicted_class": class_name,
            "predicted_class_idx": int(predicted_class),
            "confidence": round(float(confidence), 4),
            "confidence_level": confidence_level,
            "confidence_message": confidence_message,
            
            # Classification
            "tier": class_info['tier'],
            "severity": template.get('severity', class_info['severity']),
            "emoji": template.get('emoji', '❓'),
            "tagline": template.get('tagline', f'{class_name} Detected'),
            
            # Action
            "action": template.get('action', 'CONSULT A DOCTOR'),
            "urgency_message": template.get('urgency_message', ''),
            "description": template.get('description', ''),
            
            # Care advice
            "care_advice": template.get('care_advice', []),
            "risk_factors": template.get('risk_factors', []),
            
            # Hospital
            "hospital_search_query": template.get('hospital_search_query', 'dermatologist near me'),
            "hospital_type": template.get('hospital_type', 'Dermatology Clinic'),
            
            # Differential diagnosis
            "differential_diagnosis": differential,
            "close_call": close_call,
            
            # Cancer alert
            "cancer_alert": cancer_alert,
            "cancer_in_differential": cancer_in_top3,
            
            # All probabilities (for chart)
            "all_probabilities": {
                self.class_names[i]: round(float(all_probabilities[i]), 4)
                for i in range(self.num_classes)
            },
            
            # Disclaimer
            "disclaimer": (
                "⚠️ IMPORTANT: This is an AI-assisted analysis tool for educational purposes only. "
                "It is NOT a substitute for professional medical diagnosis. The accuracy of AI predictions "
                "can vary. Always consult a qualified dermatologist or healthcare professional for "
                "proper diagnosis and treatment. If you notice any suspicious changes in your skin, "
                "please seek medical attention promptly."
            ),
        }
        
        # ── Override: If cancer probability is high, ALWAYS warn ──
        if cancer_alert and class_info['tier'] not in ['CANCER', 'PRE-CANCER']:
            highest_cancer = max(cancer_in_top3, key=lambda x: x['probability'])
            response['cancer_warning'] = (
                f"⚠️ Note: While the top prediction is {class_name}, "
                f"the model also detected a {highest_cancer['probability']:.0%} probability of "
                f"{highest_cancer['class_name']} ({highest_cancer['tier']}). "
                f"We strongly recommend consulting a dermatologist to rule out any malignancy."
            )
        
        return response
    
    def get_severity_color(self, severity: str) -> str:
        """Return color hex code for severity level."""
        colors = {
            "CRITICAL": "#e74c3c",
            "HIGH": "#e67e22",
            "MEDIUM": "#f39c12",
            "LOW": "#27ae60",
        }
        return colors.get(severity, "#95a5a6")
    
    def get_tier_color(self, tier: str) -> str:
        """Return color hex code for tier."""
        colors = {
            "CANCER": "#e74c3c",
            "PRE-CANCER": "#f39c12",
            "BENIGN": "#27ae60",
            "DISEASE": "#3498db",
        }
        return colors.get(tier, "#95a5a6")