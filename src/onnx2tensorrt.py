import torch
from plgaze.models import create_model
from omegaconf import DictConfig

# Load the configuration
config = DictConfig.load('/home/kyv/Desktop/Capstone/WebCamGazeEstimation/src/plgaze/data/configs/eth-xgaze.yaml')

# Initialize the model
model = create_model(config)
checkpoint = torch.load(config.gaze_estimator.checkpoint, map_location='cpu')
model.load_state_dict(checkpoint['model'])
model.eval()

# Create dummy input matching the input size of your model
dummy_input = torch.randn(1, 3, 224, 224)  # Adjust dimensions as needed

# Export the model to ONNX format
torch.onnx.export(model, dummy_input, "gaze_estimator.onnx", verbose=True)
