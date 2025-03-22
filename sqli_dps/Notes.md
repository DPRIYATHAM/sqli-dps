# Plan

- Train a ml model using scikit learn
- save the parameters 
- implement the model in c, initially use ctypes for ILC and then after this convert cytpes into cython 
- implement a request api to get the model parameters

# Implementing ILC using ctypes

### Compiling C programs

```bash
clang -shared -fPIC -o {file}.so {file}.c
```

or
```bash
gcc -shared -fPIC -o {file}.so {file}.c
```

### using c procedures in python

```python
import ctypes
import time
# import my_c_code
TEST_SIZE = 1_000_000

my_c_code = ctypes.CDLL('./check.so')

my_c_code.adder.argtypes = (ctypes.c_int,)
my_c_code.adder.restyp = ctypes.c_int
start = time.time()
my_c_code.add(TEST_SIZE)
end = time.time()

c_time = (end - start) * 1000

print(f"C Execution Time: {c_time}ms")

start = time.time()
ans = 0
for i in range(TEST_SIZE):
    ans += i
end = time.time()
python_time = (end - start) * 1000
print(f"Python Execution Time: {python_time}ms")

print(f"C is faster by {(python_time - c_time) / python_time * 100:.2f}%")
```


# Finding
> Result: 93% faster Execution found for 1 Billion addition operation (ctypes)

> Cython turned out to be 98% faster for 1 Billion addition Operations

> For Multinomial Naive Bayes with 2 classes (payload, not payload) and 1000 features
> The Inference time were 23.9ms

> Hypothesis: for Multinomial Naive Bayes model with 2 classes and 1000 features implemented in C 
> and used through ILC we can expect an inference time of 24 * 0.07 = 1.44ms (Ctypes) and 
> 24 * 0.02 = 0.48ms for Cython