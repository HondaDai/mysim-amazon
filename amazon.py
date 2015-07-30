
import boto.ec2
import time
import os

region = 'us-west-2'
ec2 = boto.ec2.connect_to_region(region)


def create_image(inst):
  t = time.strftime("%Y-%m-%d/%H-%M-%S", time.localtime())
  img_name = "%s/%s" % (inst.id, t)
  img_id = inst.create_image(name=img_name, no_reboot=True)
  return (img_name, img_id)

def pick(k, instances=None):
  if instances == None:
    instances = get_all_instances()
  return [getattr(inst, k) for inst in instances]

def get_all_instances():
  return [i for r in ec2.get_all_instances() for i in r.instances ]

# def get_instance_id(inp):
#   if inp.__class__ == boto.ec2.instance.Reservation:
#     return get_instance_id(inp.instances[0])
#   else:
#     return inp.id

# def get_instance_status(inp):
#   return ec2.get_all_instance_status(
#     instance_ids=[get_instance_id(inp)], 
#     include_all_instances=True
#   )[0]

def get_my_images():
  return ec2.get_all_images(owners=['self'])


def show_instance_info(inst):
  keys = ['id', 'image_id', 'state', 'ip_address', 'instance_type', 'launch_time', 'placement' , 'key_name', 'subnet_id', 'groups']
  for k in keys:
    if k == "groups":
      group_names = [g.name for g in getattr(inst, k)]
      print "{:>20}: {}".format(k, str(group_names))
    else:
      print "{:>20}: {}".format(k, getattr(inst, k))


def clone_instances(inst, num=1, delete_image=False, start_instance=False):
  '''
    num:             number of clone
    delete_image:    delete image after clone
    start_instance:  start_instance after clone
  '''
  return ec2.run_instances(
    image_id='ami-f52f1dc5', 
    instance_type='t2.micro', 
    key_name='aws-ec2')


def stop_all():
  return [i.stop() for i in get_all_instances()]

def start_all():
  return [i.start() for i in get_all_instances()]

def state_all():
  return [i.state for i in get_all_instances()]

def get_all_names():
  return [i.tags['Name'] for i in get_all_instances()]

def get_instance(name):
  return [i for i in get_all_instances() if i.tags['Name'] == name][0]

def wait_state(name, state):
  while get_instance(name).state != state:
    time.sleep(2)
  return True

# def postgres_ip():
#   return get_instance('Postgres').ip_address

# def reload():
#   execfile('amazon.py')

def ssh_to(name, autostart=False):
  if autostart:
    get_instance(name).start()
    wait_state(name, 'running')
  os.system("ssh -i /Volumes/Transcend/ns-allinone-3.21/aws-ec2.pem ubuntu@%s" % (get_instance(name).ip_address) )

def sftp_to(name, autostart=False):
  if autostart:
    get_instance(name).start()
    wait_state(name, 'running')
  os.system("sftp -i /Volumes/Transcend/ns-allinone-3.21/aws-ec2.pem ubuntu@%s" % (get_instance(name).ip_address) )

# ssh_to("Postgres")


# inst = ec2.get_all_instances()
