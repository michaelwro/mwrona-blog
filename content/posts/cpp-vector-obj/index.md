---
title: "A Custom Vector Class for Embedded C++ Applications"
date: "2021-09-13"
author: Michael Wrona
draft: false
tags: ["numerical methods", "coding", "c++"]
---

## Introduction

Learning how to use [arrays in C++](https://www.cplusplus.com/doc/tutorial/arrays/) is an extremely important skill to have as a programmer. Generally speacking, arrays are used to store data with identical types as a group. The simplest and most commonly used array is a [vector](https://en.wikipedia.org/wiki/Vector), or 1D array. Creating, deallocating, and keeping track of array lengths can complicate programming. The C++ standard library has a very good implementation of a [vector object](https://en.cppreference.com/w/cpp/container/vector), is somewhat bloated and complex for use in embedded applications. `std::vector` is also a template, which are not very kosher in the world of embedded programming. The [quadcopter flight software](https://github.com/michaelwro/HummingbirdFCU) I'm developing requires vectors of many different lengths and would be complex to manage. Therefore, here is a simplified vector class for creating and managing vectors for embedded C++ projects.

Full source code for my vector class can be found on my GitHub repo.

## Functionality

My vector class has the following capabilities:

* Create/allocate the vector in memory with a fixed size
* Deallocate the vector once it goes out of scope
* Return the length (number of elements)
* Fill the vector with a number
* Return the magnitude/norm

I will create a `float` vector class, but could be easily modifed by replacing `float` with `double`, `uint32_t`, etc.

## Constructor - Creating the Vector

The constructor is what is called when we create a vector object. The input to a vector object will be it's length, or the number of elements. The constructor also allocates the vector's array in memory. Critical embedded applications often use static arrays only, but I chose to allocate the array in my microcontroller's heap memory. I implemented both in code, so you can choose which one you prefer.

```cpp

/**
 * Create a float vector object.
 *
 * @param vecLen Length of vector, number of elements in the array.
 */
Vectorf::Vectorf(size_t vecLen)
{
    // Check if len is 
    this->n = vecLen;
}


```

