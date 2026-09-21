import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

def simulate_training_metrics(epochs: int) -> Tuple[List[float], List[float]]:
    """
    Simulates training and validation loss/accuracy over given epochs,
    incorporating basic validation against corrupted or infinite metrics.
    """
    if epochs <= 0:
        raise ValueError("Epochs must be greater than zero.")

    # Generate synthetic training loss with a downward trend
    np.random.seed(42)
    base_loss = np.linspace(2.0, 0.1, epochs)
    noise = np.random.normal(0, 0.05, epochs)
    training_loss = base_loss + noise

    # Security check: Ensure no negative or infinite loss values exist (Data Sanitization)
    training_loss = np.clip(training_loss, 0.01, None)
    if np.any(np.isnan(training_loss)) or np.any(np.isinf(training_loss)):
        raise ValueError("Critical error: Loss metrics contain NaN or Infinite values.")

    # Generate corresponding accuracy metrics
    accuracy = np.linspace(50.0, 98.5, epochs) + np.random.normal(0, 1.0, epochs)
    accuracy = np.clip(accuracy, 0.0, 100.0)

    return training_loss.tolist(), accuracy.tolist()

def plot_training_progress(loss: List[float], acc: List[float]) -> None:
    """
    Plots the training loss and accuracy using Matplotlib with clean configurations.
    """
    epochs_range = range(1, len(loss) + 1)

    plt.figure(figsize=(10, 5))

    # Plot Loss Curve
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, loss, color='red', linewidth=2, label='Training Loss')
    plt.title('Model Loss Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss Value')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Plot Accuracy Curve
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, acc, color='green', linewidth=2, label='Accuracy (%)')
    plt.title('Model Accuracy Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy Percentage')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    plt.tight_layout()
    plt.show()
    print("Training progress visualization successfully rendered.")

if __name__ == "__main__":
    total_epochs = 20
    print(f"Starting tracking simulation for {total_epochs} epochs...")
    
    losses, accuracies = simulate_training_metrics(total_epochs)
    plot_training_progress(losses, accuracies)