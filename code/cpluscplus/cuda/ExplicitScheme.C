#include "ExplicitScheme.h"

#include <iostream>

#include "ExplicitSchemeCuda.h"
#include <cuda_runtime.h>

#define POLY2(i, j, imin, jmin, ni) (((i) - (imin)) + (((j)-(jmin)) * (ni)))

ExplicitScheme::ExplicitScheme(const InputFile* input, Mesh* m) :
	mesh(m)
{
	int nx = mesh->getNx()[0];
	int ny = mesh->getNx()[1];
}

void ExplicitScheme::doAdvance(const double dt)
{
	diffuse(dt);

	reset();

	updateBoundaries();
}

void ExplicitScheme::updateBoundaries()
{
	for (int i = 0; i < 4; i++) {
		reflectBoundaries(i);
	}
}

void ExplicitScheme::init()
{
	updateBoundaries();
}

void ExplicitScheme::reset()
{
	double* u0 = mesh->getU0();
	double* u1 = mesh->getU1();

	int nx = mesh->getNx()[0] + 2;
	int ny = mesh->getNx()[1] + 2;

	const size_t N = nx*ny;

	resetCudaKernel(u0,u1,N);
}

void ExplicitScheme::diffuse(double dt)
{
	double* u0 = mesh->getU0();
	double* u1 = mesh->getU1();
	int x_min = mesh->getMin()[0];
	int x_max = mesh->getMax()[0];
	int y_min = mesh->getMin()[1]; 
	int y_max = mesh->getMax()[1]; 
	double dx = mesh->getDx()[0];
	double dy = mesh->getDx()[1];

	int nx = mesh->getNx()[0] + 2;

	double rx = dt/(dx*dx);
	double ry = dt/(dy*dy);

	diffuseCudaKernel(u0, u1, x_min, x_max, y_min, y_max, nx, rx, ry);
}

void ExplicitScheme::reflectBoundaries(int boundary_id)
{
	double* u0 = mesh->getU0();
	int x_min = mesh->getMin()[0];
	int x_max = mesh->getMax()[0];
	int y_min = mesh->getMin()[1]; 
	int y_max = mesh->getMax()[1]; 

	int nx = mesh->getNx()[0] + 2;

	reflectBoundariesCudaKernel(u0, x_min, x_max, y_min, y_max, nx, boundary_id);
}
