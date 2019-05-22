#include "MeshCuda.h"

#define BLOCK_SIZE 256

#include "thrust/reduce.h"
#include "thrust/device_vector.h"

__global__
void get_total_temperature_kernel(const double* u0, double* total_temperature, const int x_min, const int x_max, const int y_min, const int y_max, const int nx)
{
	const int global_index = (blockDim.x * blockIdx.x) + threadIdx.x;
	const int row = global_index / nx;
	const int column = global_index % nx;

	__shared__ double temperature_shared[BLOCK_SIZE];
	temperature_shared[threadIdx.x] = 0.0;

	if(row >= y_min && row <= y_max && column >= x_min && column <= x_max) {
		temperature_shared[threadIdx.x] = u0[global_index];
	}

	__syncthreads();
	for (int offset = BLOCK_SIZE / 2; offset > 0; offset /= 2) {
		if (threadIdx.x < offset) {
			temperature_shared[threadIdx.x] += temperature_shared[threadIdx.x + offset];
		}
		__syncthreads();
	}

	total_temperature[blockIdx.x] = temperature_shared[0];
}


double getTotalTemperatureCudaKernel(double* u0, double* total_temperatures, int x_min, int x_max, int y_min, int y_max, int nx)
{
	const int N = (x_max - x_min + 3) * (y_max - y_min + 3);
	const int num_blocks = (N + BLOCK_SIZE - 1)/BLOCK_SIZE;

	get_total_temperature_kernel<<<num_blocks, BLOCK_SIZE>>>(u0, total_temperatures, x_min, x_max, y_min, y_max, nx);

	thrust::device_ptr<double> thrust_total_temperatures(total_temperatures);

	return thrust::reduce(thrust_total_temperatures, thrust_total_temperatures + num_blocks, 0.0);
}
