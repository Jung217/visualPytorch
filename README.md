# Visual PyTorch

Visual PyTorch is a web-based automated machine learning tool designed to simplify the creation of PyTorch models. It provides an intuitive visual interface where users can drag and drop layers, organize them into a graph structure, and automatically generate the corresponding runnable PyTorch code.

## Features

- **Visual Graph Editor**: Design your neural network architecture visually by connecting nodes.
- **Examples Library**: Quickly load pre-defined templates to get started:
  - **Classic CNN**: Convolutional Neural Networks for image tasks.
  - **RNN/LSTM**: Recurrent Neural Networks for sequence data.
  - **GAN**: DCGAN Generator and Discriminator templates.
  - **Transformers**: BERT-like Encoder stacks.
- **Comprehensive Layer Support**: Includes a wide range of standard PyTorch layers:
  - **Convolutional**: `nn.Conv2d`, `nn.ConvTranspose2d`
  - **Pooling**: `nn.MaxPool2d`, `nn.AvgPool2d`
  - **Recurrent**: `nn.RNN`, `nn.LSTM`, `nn.GRU`
  - **Linear & Activations**: `nn.Linear`, `nn.ReLU`, `nn.LeakyReLU`, `nn.Sigmoid`, `nn.Tanh`, `nn.Softmax`
  - **Normalization**: `nn.BatchNorm2d`, `nn.LayerNorm`
  - **Transformers**: `nn.Transformer`, `nn.TransformerEncoderLayer`, `nn.Embedding`
  - **Utilities**: `nn.Flatten`, `nn.Dropout`
- **Instant Code Generation**: Instantly generates valid, ready-to-run PyTorch code based on your visual design.
- **Enhanced UI Experience**:
  - **True Black Dark Mode**: High-contrast, OLED-friendly theme.
  - **Recycle Bin**: Delete nodes intuitively by dragging them to the emoji-style trash bin.
  - **Responsive Design**: Polished sidebar and property panels.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd visualPytorch
    ```

2.  **Install backend dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    # Create virtual environment (optional but recommended)
    python -m venv venv
    
    # Activate virtual environment
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate

    # Install requirements
    pip install -r backend/requirements.txt
    ```

### How to Run

1.  **Start the Backend Server:**
    Run the FastAPI server using `uvicorn` from the project root directory:
    ```bash
    uvicorn backend.main:app --reload
    ```

2.  **Access the Application:**
    Open your web browser and navigate to:
    ```
    http://127.0.0.1:8000
    ```
    This will load the Visual PyTorch editor interface.

## Project Structure

- `backend/`: Contains the FastAPI server and logic.
    - `main.py`: The entry point for the backend application.
    - `generator.py`: Logic for parsing the graph and generating PyTorch code.
    - `static/`: Contains the frontend assets (HTML, CSS, JS).
- `README.md`: This documentation file.
