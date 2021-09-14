---
title: "A Simple C++ Vector Class"
date: "2021-09-13"
author: Michael Wrona
draft: false
tags: ["coding", "c++"]
---

## Introduction

Learning how to use [arrays in C++](https://www.cplusplus.com/doc/tutorial/arrays/) is an extremely important skill to have as a programmer. Generally speacking, arrays are used to store data with identical types as a group. The simplest and most commonly used array is a [vector](https://en.wikipedia.org/wiki/Vector), or 1D array. Creating, deallocating, and keeping track of array lengths can complicate programming. The C++ standard library has a very good implementation of a [vector object](https://en.cppreference.com/w/cpp/container/vector), is somewhat bloated and complex for applications with tight memory requirements. `std::vector` is also a template, which aren't a great idea in critical applications. Therefore, here is a simplified vector class for creating and managing vectors.

Full source code for my vector class can be found on my GitHub repo.

## Functionality

My vector class has the following capabilities:

* Create/allocate the vector in memory with a fixed size
* Return the length (number of elements)
* Fill the vector with a number
* Return the magnitude/norm
* Deallocate the vector

I will create a `float` vector class, but could be easily modifed by replacing `float` with `double`, `uint32_t`, etc.

## Vector Class Declaration

The vector class is declared in it's header file. This defines the constructors, deconstructor, methods, and access specifiers for each method and variable.

```cpp
#ifndef __VECTORF_H_  // include guard
#define __VECTORF_H_

// headers
#include <iostream>
#include <stdexcept>
#include <string>

class Vectorf {
    public:
        Vectorf(size_t vecLen = 3);  // constructor
        virtual ~Vectorf();  // deconstructor
        void Fill(float val);
        size_t GetLen();

        float *vec;  ///< Vector's dynamic array
    protected:
    private:
        size_t n; ///< Vector length.
};
#endif // __VECTORF_H_
```

## Constructor - Creating the Vector

The constructor is what is called when we create a vector object. The input to a vector object will be it's length, or the number of elements. The constructor then allocates the vector's array in heap memory with the `new` keyword. We have to use dynamic arrays since the array size is unknown until runtime. I also added some error checks.

```cpp
/**
 * Create a float vector object.
 *
 * @param vecLen Length of vector, number of elements in the array. Default 3
 */
Vectorf::Vectorf(size_t vecLen) {
    size_t i;

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
        std::cerr << "Bad vectorf allocation: " << ba.what() << std::endl;
    }

    // Set initial values to zero
    this->Fill(0.0f);
}
```

## Return the Length

The following method returns the vector length, or the number of elements in the vector's array. This could be used in outside code when the length of a vector is unknown.

```cpp
/**
 * Return the length of the vector.
 * 
 * @returns Number of elements in the vector's array.
 */
size_t Vectorf::GetLen() {
    return this->n;
}
```

## Fill the Vector

The `fill()` method fills the entire array with a specified value. This method is used in the constructor to initialize the vector with all zeros.

```cpp
/**
 * Fill the entire vector with a specified value.
 * 
 * @param val Value to fill the array with.
 */
void Vectorf::Fill(float val)
{
    size_t i;

    for (i = 0; i < this->n; i++) {
        this->vec[i] = val;
    }
}
```





## Deconstructor - Deallocate Arrays

The deconstructor deallocates the vector's array after it goes out of scope. This is important so that the computer can use the array's memory locations after the vector is out of scope.

```cpp
/**
 * Deconstructor for vectorf object.
 */
Vectorf::~Vectorf() {
    delete[] this->vec; // deallocate from the heap
}
```
