#Pattern formation code

#Solves the pair of PDEs:
#       u_t = D_1 \nabla^2 u + f(u,v)
#       v_t = D_2 \nabla^2 v + g(u,v)

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import spdiags,linalg,eye

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


def five_pt_laplacian(m,a,b):
    e=np.ones(m**2)
    e2=([0]+[1]*(m-1))*m
    h=(b-a)/(m+1)
    A=np.diag(-4*e,0)+np.diag(e2[1:],-1)+np.diag(e2[1:],1)+np.diag(e[m:],m)+np.diag(e[m:],-m)
    A/=h**2
    return A

def five_pt_laplacian_sparse(m,a,b):
    e=np.ones(m**2)
    e2=([1]*(m-1)+[0])*m
    e3=([0]+[1]*(m-1))*m
    h=(b-a)/(m+1)
    A=spdiags([-4*e,e2,e3,e,e],[0,-1,1,-m,m],m**2,m**2)
    A/=h**2
    return A

#Grid
a=-1.; b=1.
m=100; h=(b-a)/m; 
x = np.linspace(-1,1,m)
y = np.linspace(-1,1,m)
Y,X = np.meshgrid(y,x)

u=np.random.randn(m,m)/2.;
v=np.random.randn(m,m)/2.;


plt.pcolormesh(x,y,u)
plt.colorbar; plt.axis('image'); plt.draw()
dt=h/delta/5.;

A=five_pt_laplacian_sparse(m,-1.,1.);
II=eye(m*m,m*m)

u=u.reshape(-1)
v=v.reshape(-1)

t=0.

plt.ion()

for k in range(300):
    #i=1:m; j=1:m; t=0;
    #i=2:m-1; j=2:m-1; t=0;
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
    u = linalg.spsolve(II-dt*delta*Du*A,u)
    v = linalg.spsolve(II-dt*delta*Dv*A,v)

    unew=u+dt*f(u,v);
    v   =v+dt*g(u,v);
    u=unew;
    t=t+dt;

    if k/3==float(k)/3:
        U=u.reshape((m,m))
        plt.pcolormesh(x,y,U)
        plt.colorbar
        plt.axis('image')
        plt.draw()

plt.ioff()
