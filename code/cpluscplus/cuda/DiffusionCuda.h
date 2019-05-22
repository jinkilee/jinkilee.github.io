#ifndef DIFFUSION_CUDA_H_
#define DIFFUSION_CUDA_H_
void initialiseCudaKernel(double* u0, int x_min, int x_max, int y_min, int y_max, int nx);

void initialiseCudaKernel(double* u0, int x_min, int x_max, int y_min, int y_max, int nx, int subregion_xmin, int subregion_xmax, int subregion_ymin, int subregion_ymax);

#endif
