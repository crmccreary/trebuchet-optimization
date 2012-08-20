import os,sys
import glob
import math
from scipy.optimize import cobyla as co
from jinja2 import Template
import subprocess

# Load templates
f = open('templates/Trebuchet.inp','r')
template_trebuchet_raw = f.read()
f.close()
template = Template(template_trebuchet_raw)

job_id = "Trebuchet"
[cw_mass_index,
 cw_beam_length_index,
 cw_length_index,
 sling_length_index]=range(4)

x_init=[]
x_init.insert(cw_mass_index, 1.0)
x_init.insert(cw_beam_length_index, 1.0)
x_init.insert(cw_length_index, 1.0)
x_init.insert(sling_length_index, 1.0)


def projectile_range(x):
    # Clean up files
    files = glob.glob('Trebuchet_run.*')
    for fname in files:
        os.remove(fname)

    # Un-normalize variables
    l1 = x[cw_beam_length_index]*0.1
    l2 = x[cw_length_index]*0.2
    l3 = 1.0 # Fix this variable
    l4 = x[sling_length_index]*1.0
    cw_mass = x[cw_mass_index]*200.0
    projectile_dict = {'mass':0.2} # Fixed, mass of orange

    cw_dict = {'mass':cw_mass,
               'x': l1*math.sqrt(2)/2,
               'y': l1*math.sqrt(2)/2-l2}
    cw_end_dict = {'x': l1*math.sqrt(2)/2,
                   'y': l1*math.sqrt(2)/2}
    sling_end_dict = {'x':-l3*math.sqrt(2)/2,
                      'y':-l3*math.sqrt(2)/2}
    sling_dict = {'x':sling_end_dict['x'] + l4,
                  'y':sling_end_dict['y']}
    raw = template.render(projectile=projectile_dict,
                          cw=cw_dict,
                          cw_end=cw_end_dict,
                          sling_end=sling_end_dict,
                          sling=sling_dict)
    f = open('Trebuchet_run.inp','wb')
    f.write(raw)
    f.close()

    # Execute abaqus
    subprocess.call(['/opt/abaqus/Commands/abaqus','interactive','job=Trebuchet_run'])
    # Extract and return weight
    subprocess.call(['/opt/abaqus/Commands/abaqus',
                     'python',
                     'projectile_range.py',
                     'Trebuchet_run'])
    f = open('Trebuchet_run_range.txt','r')
    r = float(f.readline())
    f.close()
    f = open('run_history.txt','a')
    f.write('cw = {0}, cw length = {1}, cw beam length = {2}, sling length = {3}, range = {4}\n'.format(cw_dict['mass'],l2,l1,l4,r))
    f.close()
    '''
    Since scipy optimizers can only minimize, multiply by -1
    '''
    return -1.0*r

def positive_cw_mass(x):
    return x[cw_mass_index]
def positive_cw_beam_length(x):
    return x[cw_beam_length_index]
def positive_cw_length(x):
    return x[cw_length_index]
def positive_sling_length(x):
    return x[sling_length_index]

if __name__ == '__main__':
    if os.path.exists('./run_history.txt'):
        os.remove('run_history.txt')
    print co.fmin_cobyla(projectile_range,
                         x_init,
                         [positive_cw_mass,
                          positive_cw_beam_length,
                          positive_cw_length,
                          positive_sling_length],
                         rhobeg=0.1,
                         rhoend=0.001,
                         iprint=3,
                         maxfun=40)
