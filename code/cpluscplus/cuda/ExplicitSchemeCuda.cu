#include "ExplicitSchemeCuda.h"

#define BLOCK_SIZE 256

#define POLY2(i, j, imin, jmin, ni) (((i) - (imin)) + (((j)-(jmin)) * (ni)))
__global__
void reset_with_Cuda(double* u0, double* u1, const size_t N)
{
	// Obtain index
	int idx = threadIdx.x + (blockIdx.x*blockDim.x);
	if(idx < N)
		u0[idx] = u1[idx];
}

void resetCudaKernel(double* u0, double* u1, const size_t N)
{
	// TO_DO: copy u1 to u0
	const int num_blocks = (N + BLOCK_SIZE - 1)/BLOCK_SIZE;
	reset_with_Cuda<<<num_blocks, BLOCK_SIZE>>>(u0, u1, N);
}

__global__
void diffuse_with_Cuda(double* u0, double* u1, int x_min, int x_max, int y_min, int y_max, int nx, double rx, double ry)
{
	// Obtain x and y coordinate 
	int idx  = threadIdx.x + (blockIdx.x*blockDim.x);
	int i    = idx % nx + 1;
	int j    = idx / nx + 1;
	
	// Obtain size of array
	int size = (x_max - x_min + 3) * (y_max - y_min + 3);

	if(idx < size) {
		if((x_min <= i && i <= x_max) && (y_min <= j && j <= y_max)) {
			int n1 = POLY2(i,   j,   x_min-1, y_min-1, nx);
			int n2 = POLY2(i-1, j,   x_min-1, y_min-1, nx);
			int n3 = POLY2(i+1, j,   x_min-1, y_min-1, nx);
			int n4 = POLY2(i,   j-1, x_min-1, y_min-1, nx);
			int n5 = POLY2(i,   j+1, x_min-1, y_min-1, nx);

			u1[n1] = (1.0 - 2.0*rx - 2.0*ry)*u0[n1] + rx*u0[n2] + rx*u0[n3] + ry*u0[n4] + ry*u0[n5];
		}
	}
}

void diffuseCudaKernel(double* u0, double* u1, int x_min, int x_max, int y_min, int y_max, int nx, double rx, double ry)
{
	// TO_DO: diffusion!
	const int N = (x_max - x_min + 3) * (y_max - y_min + 3);
	const int num_blocks = (N + BLOCK_SIZE - 1)/BLOCK_SIZE;

	diffuse_with_Cuda<<<num_blocks, BLOCK_SIZE>>>(u0, u1, x_min, x_max, y_min, y_max, nx, rx, ry);
} 

__global__
void reflectBoundaries_with_Cuda(double* u0, int x_min, int x_max, int y_min, int y_max, int nx, int boundary_id)
{
	// Obtain x and y coordinate 
	int idx  = threadIdx.x + (blockIdx.x*blockDim.x);
	int i    = idx % nx + 1;
	int j    = idx / nx + 1;
	
	// Obtain size of array
	int size = (x_max - x_min + 3) * (y_max - y_min + 3);

	/* TO_DO: reflect top boundary */
	if(idx < size) {		
		if(0 == boundary_id) { // UPWARD DIRECTION
			int n1 = POLY2(i, y_max,   x_min-1, y_min-1, nx);
			int n2 = POLY2(i, y_max+1, x_min-1, y_min-1, nx);
			u0[n2] = u0[n1];
		}
		/* TO_DO: reflect right boundary */
		if(1 == boundary_id) { // RIGHT DIRECTION
			int n1 = POLY2(x_max,   j, x_min-1, y_min-1, nx);
			int n2 = POLY2(x_max+1, j, x_min-1, y_min-1, nx);
			u0[n2] = u0[n1];
		}
		/* TO_DO: reflect bottom boundary */
		if(2 == boundary_id) { // DOWNWARD DIRECTION
			int n1 = POLY2(i, y_min,   x_min-1, y_min-1, nx);
			int n2 = POLY2(i, y_min-1, x_min-1, y_min-1, nx);
			u0[n2] = u0[n1];
		}
		/* TO_DO: reflect left boundary */
		else {//3 == boundary_id // LEFT DIRECTION
			int n1 = POLY2(x_min,   j, x_min-1, y_min-1, nx);
			int n2 = POLY2(x_min-1, j, x_min-1, y_min-1, nx);
			u0[n2] = u0[n1];
		}
	}
}

void reflectBoundariesCudaKernel(double* u0, int x_min, int x_max, int y_min, int y_max, int nx, int boundary_id)
{
	const int N = (x_max - x_min + 3) * (y_max - y_min + 3);
	const int num_blocks = (N + BLOCK_SIZE - 1)/BLOCK_SIZE;
	reflectBoundaries_with_Cuda<<<num_blocks, BLOCK_SIZE>>>(u0, x_min, x_max, y_min, y_max, nx, boundary_id);
}
