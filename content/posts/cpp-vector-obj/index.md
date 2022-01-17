---
title: "A Simple C++ Vector Class"
date: "2021-09-14"
author: Michael Wrona
draft: false
tags: ["coding", "c++"]
---

## Introduction

Learning how to use [arrays in C++](https://www.cplusplus.com/doc/tutorial/arrays/) is an extremely important skill to have as a programmer. Generally speaking, arrays are used to store data with identical types as a group. The simplest and most commonly used array is a [vector](https://en.wikipedia.org/wiki/Vector), or 1D array. Creating, deallocating, and keeping track of array lengths can complicate programming. The C++ standard library has a very good implementation of a [vector object](https://en.cppreference.com/w/cpp/container/vector), but is somewhat bloated for applications with tight memory requirements. `std::vector` is also a template, which aren't kosher in embedded and critical applications. Therefore, here is a simplified vector class for creating and managing vectors that I created.

Full source code for my vector class can be found on my [GitHub repo](https://github.com/michaelwro/simple-vectorf).

## Functionality

My vector class has the following capabilities:

* Create/allocate the vector in memory with a fixed size
* Return the length (number of elements)
* Return elements of the vector
* Fill the vector with a constant
* Return the magnitude/norm
* Deallocate the vector

I will create a `float` vector class, but the code could be easily modifed by replacing `float` with `double`, `uint32_t`, etc.

## Vector Class Declaration

The vector class is declared in it's header file. This defines the constructor, deconstructor, methods, and access specifiers for each method and variable.

```cpp
class Vectorf {
    public:
        Vectorf(size_t vecLen = 3);
        ~Vectorf();
        void Fill(float val);
        void Print();
        size_t GetLen();
        float Get(size_t index);
        float GetNorm();
    protected:
    private:
        size_t n; ///< Vector length
        float *vec;  ///< Vector's dynamic array
};
```

## Constructor - Creating the Vector

The constructor is called when we create a vector object. The input when creating a vector object will be it's length, or the number of elements. The constructor then allocates the vector's array in heap memory with the `new` keyword. We have to use dynamic arrays since the array size is unknown until runtime. I added some error checks, too.

```cpp
Vectorf::Vectorf(size_t vecLen) {
    // Check if len is zero
    if (vecLen == (size_t)0) {
        throw std::invalid_argument("Vector length must be greater than zero");
    }

    this->n = vecLen;  // vector length

    // check for bad allocation
    try {
        this->vec = new float[this->n];  // Allocate array on the heap
    }
    catch (const std::bad_alloc &ba) {
        std::cerr << "Bad vectorf array allocation: " << ba.what() << std::endl;
    }

    // Set initial values to zero
    this->Fill(0.0f);
}
```

## Return the Length

The following method returns the vector length, or the number of elements in the vector's array. This could be used in external code when the length of a vector is unknown.

```cpp
size_t Vectorf::GetLen() {
    return this->n;
}
```

## Get a Value

The `Get()` method returns the vector's value at the specified index. It also ensures the specified index is less than the vector's length.

```cpp
float Vectorf::Get(size_t index) {
    // check the specified index
    if (index > this->n) {
        throw std::invalid_argument("Vector index exceeded length.");
        return 0.0f;  // just in case
    }

    return this->vec[index];
}
```


## Fill the Vector

The `fill()` method fills the entire array with a specified value. This method is also used in the constructor to initialize the vector with all zeros.

```cpp
void Vectorf::Fill(float val) {
    size_t i;

    for (i = 0; i < this->n; i++) {
        this->vec[i] = val;
    }
}
```

## Compute Vector Magnitude

The `GetNorm()` method computes the magnitude, or norm, of the vector. The mangitude is the square root of the sum of of the vector elements, squared.

$$ norm = \sqrt{x_0^2 + x_1^2 + x_2^2 + ...} $$

```cpp
float Vectorf::GetNorm() {
    size_t i;
    float sum = 0.0f;

    // Sum of the squares
    for (i = 0; i < this->n; i++)
        sum += this->vec[i] * this->vec[i];

    // return the square root
    return sqrtf(sum);
}
```

## Print the Vector

The `Print()` method prints the entire vector to the console. This could be useful for debugging purposes.

```cpp
void Vectorf::Print() {
    size_t i;

    std::cout << "[ ";  // Left bracket
    for (i = 0; i < this->n; i++)
        std::cout << this->vec[i] << " ";  // space between elements
    std::cout << "]" << std::endl;  // right bracket
}
```

## Deconstructor - Deallocate Arrays

The deconstructor deallocates the vector's array after it goes out of scope. This is important so that the computer can use the array's memory locations after the vector is out of scope.

```cpp
Vectorf::~Vectorf() {
    delete[] this->vec; // deallocate from the heap
}
```

The source code plus an example can be found at [this GitHub repo](https://github.com/michaelwro/simple-vectorf). I hope this was useful and gave you some inspiration for your C++ projects!
