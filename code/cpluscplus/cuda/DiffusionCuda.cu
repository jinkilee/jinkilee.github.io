#include "DiffusionCuda.h"

#define BLOCK_SIZE 256

#define POLY2(i, j, imin, jmin, ni) (((i) - (imin)) + (((j)-(jmin)) * (ni)))

__global__
void init_with_Cuda(double* u0, int x_min, int x_max, int y_min, int y_max, int nx)
{
	// Obtain size of array
	int idx = threadIdx.x + (blockIdx.x*blockDim.x);
	int size = (x_max - x_min + 3) * (y_max - y_min + 3);

	if(idx < size)
		u0[idx] = 0.0;
}

__global__
void init_with_Cuda(double* u0, int x_min, int x_max, int y_min, int y_max, int nx, int sub_xmin, int sub_xmax, int sub_ymin, int sub_ymax)
{
	// Obtain x and y coordinate 
	int idx = threadIdx.x + (blockIdx.x*blockDim.x);
	int i    = idx % nx;
	int j    = idx / nx;
	
	// Obtain size of array
	int size = (x_max - x_min + 3) * (y_max - y_min + 3);

	if(idx < size) {
		// If in the subregion
		if( (sub_xmin < i && i <= sub_xmax) && (sub_ymin < j && j <= sub_ymax) )
			u0[idx] = 10.0;
		// Not in the subregion
		else
			u0[idx] = 0.0;
	}
}

void initialiseCudaKernel(double* u0, int x_min, int x_max, int y_min, int y_max, int nx)
{
	// TO_DO: initialise u0 to 0.0
	const int N = (x_max - x_min + 3) * (y_max - y_min + 3);
	const int num_blocks = (N + BLOCK_SIZE - 1)/BLOCK_SIZE;

	// If the cell is NOT in subregion,
	// Call init_with_Cuda to initialize u0 with 0.0 (Performed with GPU)
	init_with_Cuda<<<num_blocks, BLOCK_SIZE>>>(u0, x_min, x_max, y_min, y_max, nx);
}

void initialiseCudaKernel(double* u0, int x_min, int x_max, int y_min, int y_max, int nx, int subregion_xmin, int subregion_xmax, int subregion_ymin, int subregion_ymax)
{
	// TO_DO: initialise u0 to 10.0 in subregion, 0.0 elsewhere subregion indices are array rows/columns
	const int N = (x_max - x_min + 3) * (y_max - y_min + 3);
	const int num_blocks = (N + BLOCK_SIZE - 1)/BLOCK_SIZE;

	// If the cell is in subregion,
	// Call init_with_Cuda to initialize u0 with 10.0 (Performed with GPU)

	init_with_Cuda<<<num_blocks, BLOCK_SIZE>>>(u0, x_min, x_max, y_min, y_max, nx, subregion_xmin, subregion_xmax, subregion_ymin, subregion_ymax);
}

