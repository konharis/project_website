# A Fully Convolutional Neural Network for Cardiac Segmentation

A Keras implementation of the FCN model proposed in the arXiv paper [A Fully Convolutional Neural Network for Cardiac Segmentation in Short-Axis MRI
](https://arxiv.org/abs/1604.00494).

## Results


## Requirements
The code is tested on Ubuntu 14.04 with the following components:

### Software

* Python 2.7
* Keras 2.0.2 using TensorFlow GPU 1.0.1 backend
* CUDA 8.0 with CuDNN 5.1
* OpenCV 3.1
* h5py 2.7
* NumPy 1.11
* PyDicom 0.9.9
* Scikit-Image 0.13

### Datasets

* [Sunnybrook](http://smial.sri.utoronto.ca/LV_Challenge/Downloads.html)
* [Sunnybrook](http://smial.sri.utoronto.ca/LV_Challenge/Downloads.html)

## Usage
For training and evaluation, execute the following in the same directory where the datasets reside:

```bash
# Train the FCN model on the Sunnybrook dataset with 50 epochs
$ bash train_models.sh Sunnybrook 50

# Train the FCN model on the Lund Tufvesson dataset with 50 epochs
$ bash train_models.sh Lund1 50
```

The flag `<i/o>` indicates inner endocardium and outer epicardium, respectively.

To test the models on the test datasets, execute the following:

```bash
# Test Sunnybrook model for the Sunnybrook dataset
$ bash test_model.sh Lund1 model_logs/

# Create submission files for the LVSC dataset
$ bash test_model.sh Sunnybrook
```

