import macgputils
import torch  # or any other framework you're using

# Load a sample AI model (e.g., PyTorch)
model = torch.nn.Sequential(
    torch.nn.Linear(10, 10),
    torch.nn.ReLU(),
    torch.nn.Linear(10, 1)
)

# Sample input data (adjust based on your model)
input_data = torch.randn(1, 10)

# Get multiple samples
for sample in macgputils.get_gpu_stats(samples=3):
    # Execute a forward pass in the model
    output = model(input_data)
    print("Model output:", output)
    print("GPU stats:", sample)
