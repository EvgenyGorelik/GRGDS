# GRGDS
Program for compensating intensity shift between electron diffraction experiments

## Requirements

Required [Python](https://www.python.org) version >= 3.8

Install requirements using

```
pip install -r requirements.txt
```

## Usage

Call program 

```
python main.py data
```

with `data` being the directory, where the `.hkl` files are stored.

To cap the number of samples used for the calculation of the coefficients use the `--max_samples` argument. To store the images of intensities plotted against each other set the storage path using `--save_figures`.

A call that caps the number of smaples to 1000 random picked hkl values and stores the resulting images in `ìmages` looks like this:

```
python main.py data --max_samples 1000 --save_figures images
```

The results are stored in a created `results` folder.


## Background

The program calculates intersection set of hkl values in two files $a$, $b$ and fits the values $p_1$ and $p_2$ of the function

$f(p) = p_1 + p_2\cdot I_a$

so the mean squared error

$\sum_{i=1}^N (I_b - f(p))^2$

is minimized.
