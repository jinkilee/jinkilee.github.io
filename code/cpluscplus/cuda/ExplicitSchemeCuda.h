#ifndef EXPLICIT_SCHEME_CUDA_H_
#define EXPLICIT_SCHEME_CUDA_H_
void resetCudaKernel(
    double* u0,
    double* u1,
    const size_t N);

void diffuseCudaKernel(
    double* u0,
    double* u1,
    int x_min,
    int x_max,
    int y_min,
    int y_max,
    int nx,
    double rx,
    double ry);

void reflectBoundariesCudaKernel(
    double* u0,
    int x_min,
    int x_max,
    int y_min,
    int y_max,
    int nx,
    int boundary_id);
#endif
