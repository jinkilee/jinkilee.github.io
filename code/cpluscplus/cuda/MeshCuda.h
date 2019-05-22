#ifndef MESH_CUDA_H_
#define MESH_CUDA_H_

double getTotalTemperatureCudaKernel(double* u0, double* total_temperatures, int x_min, int x_max, int y_min, int y_max, int nx);

#endif
