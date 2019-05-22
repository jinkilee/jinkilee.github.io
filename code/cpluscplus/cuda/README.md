---
title: "CUDA Assignment"
date: 2019-05-22 23:24:00 -0400
categories: jekyll update
---

Implementation with Cuda
---------------
The list of Kernel function to implement is listed on the following table.

| Kernel function name        | Called by                    | Executed by |
| --------------------------- |:----------------------------:|:-----------:|
| init_with_Cuda              | initialiseCudaKernel         | GPU         |
| reset_with_Cuda             | resetCudaKernel              | GPU         |
| diffuse_with_Cuda           | diffuseCudaKernel            | GPU         |
| reflectBoundaries_with_Cuda | reflectBoundariesCudaKernel  | GPU         |

#### Initialize_with_Cuda
To initialize u0 array with 0.0 and 10.0(for subregion) inside kernel function, I take advantage of threadIdx, blockIdx and blockDim, each of which are Cuda keywords to get the thread number, block number and the number of threads in one block, respectively. Assuming that threads are formed in 1-Dimension, the index of array can be obtained by performing the following

```cpp
int index = threadIdx.x + (blockIdx.x*blockDim.x);
```

If the index is less than the number of cells in u0, I performed some initialization. This is because when deqn runs, threads can be created more than I actually need. 

```cpp
if(index < N) {
   // Performs initialization task
}
```

From the index, I can get 2D coordinate by using moduler and division operator. If the index is modulered by nx(the size of horizontal array), x coordinate can be obtained. And the index is divided by nx, y coordinate can be obtained.

```cpp
int x = index % nx;  	// get x coordinate
int y = index / nx;  	// get y coordinate
```

By comparing x and y with subregion, I can decide whether a cell should be initialized with 0.0 or 10.0.

#### reset_with_Cuda
This function can be implemented very similar as Initialize_with_Cuda. By obtaining index from threadIdx and threadBlock, u0 and u1 can be directly accessible.

### diffuse_with_Cuda
This function can be performed by getting the index of neighboring cell. To get the index of neighbors, POLY2 should be called with respect to coordinates.

```cpp
// diffuse_with_Cuda
if((x_min <= i && i <= x_max) && (y_min <= j && j <= y_max)) {
	int n1 = POLY2(i,   j,   x_min-1, y_min-1, nx);
	int n2 = POLY2(i-1, j,   x_min-1, y_min-1, nx);
	int n3 = POLY2(i+1, j,   x_min-1, y_min-1, nx);
	int n4 = POLY2(i,   j-1, x_min-1, y_min-1, nx);
	int n5 = POLY2(i,   j+1, x_min-1, y_min-1, nx);
	u1[n1] = (1.0 - 2.0*rx - 2.0*ry)*u0[n1] + rx*u0[n2] + rx*u0[n3] + ry*u0[n4] + ry*u0[n5]; }
```


### reflectBoundaries_with_Cuda
This function should be performed to calculate right temperature of boundary cells. Because the idea of dealing with each direction is same, I am going to explain only UPWARD direction, and the rest of direction can be implemented with the same idea.
To calculate the UPWARD direction, boundary_id should be equal to 0. If the boundary_id is 0, reflectBoundaries_with_Cuda will be called. Inside the kernel function, x and y coordinate should be calculated first. In case of UPWARD direction, only x coordinate will be used with POLY2 because y coordinate always should be y_max for UPWARD direction.

```cpp
// reflectBoundaries_with_Cuda
if(0 == boundary_id) {
	int n1 = POLY2(i, y_max,   x_min-1, y_min-1, nx);
	int n2 = POLY2(i, y_max+1, x_min-1, y_min-1, nx);
	u0[n2] = u0[n1]; }
// reflectBoundariesCudaKernel
const int num_blocks = (N + BLOCK_SIZE - 1)/BLOCK_SIZE;
reflectBoundaries_with_Cuda<<<num_blocks, BLOCK_SIZE>>>(u0, x_min, x_max, y_min, y_max, nx, boundary_id);
```

Likewise, RIGHT, DOWNWARD, LEFT direction also can be implemented with exactly same idea, but with different parameters to POLY2.

Result and Comparison
---------------
Cuda implementation of deqn can be measured per kernel. By comparing the execution time of each kernel, I could get the following result.
![Figure 1](http://jinkilee.github.io/img/cuda/fig1.png)
|:--:|
| *Figure 1: Per-Kernel Execution Time* |

From the above graph, I can note that I can obtain high performance with Cuda implementation, because each tread is supposed to run only one iteration of for loop. By comparing execution time with other implementation of deqn, Cuda shows the highest performance with 0.5088 seconds for big_square.in.

![Figure 2](http://jinkilee.github.io/img/cuda/fig2.png)
|:--:|
| *Figure 2: Time Comparision between different implementation* |
