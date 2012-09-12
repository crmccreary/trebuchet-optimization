import sys, getopt, os, string, math
from odbAccess import *
from abaqusConstants import *

def release_time(odb):
    '''
    Angle is initially at pi/4. Assuming that the release
    angle is when the sling is co-linear with the beam,
    The release time will be when the relative angle
    is 3*pi/4
    '''
    step=odb.steps[odb.steps.keys()[-1]]
    rel_angle_data=step.historyRegions['Element ASSEMBLY.15'].historyOutputs['CUR3'].data
    for t,rel_angle in rel_angle_data:
        if abs(rel_angle) >= 3*math.pi/4:
            return t

def axle_angle_at_release(odb, t_release):
    '''
    The beam is initially at an angle of -pi/4 from the horizontal.
    So the axle angle and thus the sling angle from horizontal
    at release will be the abs(relative angle) - pi/4
    '''
    step=odb.steps[odb.steps.keys()[-1]]
    rel_angle_data=step.historyRegions['Element ASSEMBLY.17'].historyOutputs['CUR3'].data
    for t,rel_angle in rel_angle_data:
        if t >= t_release:
            print('axle relative angle = {0}'.format(rel_angle))
            return abs(rel_angle) - math.pi/4

def frame_at_time(odb, t):
    step=odb.steps[odb.steps.keys()[-1]]
    for i, f in enumerate(step.frames):
        if f.frameValue >= t:
            return i

def velocity_at_release(odb, frame_index):
    projectile_set = odb.rootAssembly.nodeSets['PROJECTILE']
    step=odb.steps[odb.steps.keys()[-1]]
    frame = step.frames[frame_index]
    fo = frame.fieldOutputs['V']
    fo_subset = fo.getSubset(region=projectile_set)
    velocities = fo_subset.values[0].data
    return velocities[0],velocities[1]

def height_at_release(odb, frame_index):
    projectile_set = odb.rootAssembly.nodeSets['PROJECTILE']
    step=odb.steps[odb.steps.keys()[-1]]
    frame = step.frames[frame_index]
    fo = frame.fieldOutputs['U']
    fo_subset = fo.getSubset(region=projectile_set)
    y_0 = fo_subset.values[0].data[1]
    print('y_0 = {0}'.format(y_0))
    return y_0

def projectile_range(v,axle_angle,y_0):
    theta = math.pi/2 - axle_angle
    print('theta = {0}'.format(theta))
    v_mag = math.sqrt(v[0]**2 + v[1]**2)
    print('v_mag = {0}'.format(v_mag))
    g = 9.81
    d = v_mag*math.cos(theta)/g*(v_mag*math.sin(theta)+
                                    math.sqrt(v_mag**2*math.sin(theta)**2 +
                                              2*g*y_0))
    print('range = {0}'.format(d))
    return d

def output(JobID, value):
    dest = JobID + "_range.txt"
    output = open(dest,"w")
    output.write('%f\n'%(value,))
    output.close()

if __name__ == '__main__':
    # Get command line arguments.

    usage = "usage: abaqus python range.py <job name>"
    optlist, args = getopt.getopt(sys.argv[1:],'')
    JobID = args[0]
    odbPath = JobID + '.odb'
    print JobID
    print odbPath
    if not odbPath:
        print usage
        sys.exit(0)
    if not os.path.exists(odbPath):
        print "odb %s does not exist!" % odbPath
        sys.exit(0)

    odb = openOdb(path=odbPath)
    t_release = release_time(odb)
    print('release time = {0}'.format(t_release))
    axle_angle = axle_angle_at_release(odb, t_release)
    print('axle angle = {0}'.format(axle_angle))
    frame_index = frame_at_time(odb, t_release)
    print('frame index = {0}'.format(frame_index))
    y_0 = height_at_release(odb, frame_index)
    v = velocity_at_release(odb, frame_index)
    r = projectile_range(v,axle_angle,y_0)
    output(JobID, r)
    odb.close()
