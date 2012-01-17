#Pattern formation code

#Solves the pair of PDEs:
#       u_t = D_1 \nabla^2 u + f(u,v)
#       v_t = D_2 \nabla^2 v + g(u,v)

import numpy as np
import matplotlib.pyplot as plt

#Parameter values
Du=0.500; Dv=1;
delta=0.0045; tau1=0.02; tau2=0.2; alpha=0.899; beta=-0.91; gamma=-alpha;
#delta=0.0045; tau1=0.02; tau2=0.2; alpha=1.9; beta=-0.91; gamma=-alpha;
#delta=0.0045; tau1=2.02; tau2=0.; alpha=2.0; beta=-0.91; gamma=-alpha;
#delta=0.0021; tau1=3.5; tau2=0; alpha=0.899; beta=-0.91; gamma=-alpha;
#delta=0.0045; tau1=0.02; tau2=0.2; alpha=1.9; beta=-0.85; gamma=-alpha;
#delta=0.0001; tau1=0.02; tau2=0.2; alpha=0.899; beta=-0.91; gamma=-alpha;
#delta=0.0005; tau1=2.02; tau2=0.; alpha=2.0; beta=-0.91; gamma=-alpha; nx=150;

#Brusselator:
# a=3; b=10.2; Du=3.8; Dv=10; delta=1/900;
# a=3; b=10.2; Du=5; Dv=10; delta=1/900;
# f = @(u,v) a - (b+1)*u + u.^2.*v;
# g = @(u,v) b*u - u.^2.*v;
# u=a+0.01*(randn(size(x)));
# v=b/a+0.01*(randn(size(x)));

#Ladybird
#rho_u=0.01; rho_v=0.02; mu_u=0.01; sigma_v=0.02; delta=0.0001; Du=5; Dv=250;
#kappa=0.0;
#f = @(u,v) rho_u*u.^2.*v./(1+kappa*u.^2) .* mu_u.*u;
#g = @(u,v) -rho_v*u.^2.*v./(1+kappa*u.^2) + sigma_v;
#u=rand(size(x));
#v=ones(size(x));


def f(u,v):
    return alpha*u*(1-tau1*v**2) + v*(1-tau2*u);

def g(u,v):
    return beta*v*(1+alpha*tau1/beta*u*v) + u*(gamma+tau2*v);

#Grid
nx=50.; ny=nx; dx=2/nx; dy=2/ny;
X = np.linspace(-1,1,nx)
Y = np.linspace(-1,1,ny)
Y,X = np.meshgrid(Y,X)

u=np.random.randn(x.shape)/2.;
v=np.random.randn(x.shape)/2.;


plt.pcolor(x,y,u)
plt.colorbar; plt.axis('image')
dt=dx/delta/50;

A=diffusion_A(nx);
A=A/dx^2;
II=speye(nx^2);

i=1:nx; j=1:ny; t=0;
#i=2:nx-1; j=2:ny-1; t=0;
u=reshape(u,nx*nx,1);
v=reshape(v,nx*nx,1);
for k=1:10000

#BCs:
#  u(1,:)=u(end-1,:);
#  u(end,:)=u(2,:);
#  u(:,1)=u(:,end-1);
#  u(:,end)=u(:,2);
##  Explicit diffusion:
#  u(i,j)=u(i,j) + dt*((u(i-1,j)-2*u(i,j)+u(i+1,j))/dx^2 ...
#                   + (u(i,j-1)-2*u(i,j)+u(i,j+1))/dy^2);
#  v(i,j)=v(i,j) + delta*Dv*dt*((v(i-1,j)-2*v(i,j)+v(i+1,j))/dx^2 ...
#                   + (v(i,j-1)-2*v(i,j)+v(i,j+1))/dy^2);

#Simple (1st-order) IMEX:
  u=be_step(u,delta*Du*A,dt);
  v=be_step(v,delta*Dv*A,dt);

  unew=u+dt*f(u,v);
  v   =v+dt*g(u,v);
  u=unew;
  t=t+dt;

  if floor(k/10)==k/10
    up = reshape(u,nx,ny);
    pcolor(x(i,j),y(i,j),up(i,j)); shading interp; colorbar; title(num2str(t));
    colormap(hsv); axis image
    pause(0.01);
  end
end
