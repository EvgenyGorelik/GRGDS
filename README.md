# GRGDS
Program for compensating intensity shift between electron diffraction experiments

## Requirements

Required [Python](https://www.python.org) version >= 3.8

Install requirements using

```
pip -r requirements.txt
```

## Usage

Call program 

```
python main.py data
```

with `data` being the directory, where the `.hkl` files are stored.

## Background

The program calculates intersection set of hkl values in two files $a$, $b$ and fits the values $p_1$ and $p_2$ of the function

$f(p) = p_1 + p_2\cdot I_a$

so the mean squared error

$\sum_{i=1}^N (I_b - f(p))^2$

is minimized.