import os
import time
import random
import yaml
import sys
import multiprocessing
from docker import Client
from multiprocessing import Process, Manager



with open('chaos-monkey-config.yml') as data:
    yml_config = yaml.safe_load(data)['chaos_monkey']

# Get config variable from env vars
kill_interval = int(os.getenv('KILL_INTERVAL', yml_config['kill']['interval']))
start_interval = int(os.getenv('START_INTERVAL', yml_config['start']['interval']))
kill_workers = int(os.getenv('KILL_WORKERS', yml_config['kill']['workers']))
start_workers= int(os.getenv('START_WORKERS', yml_config['start']['workers']))
kill_exempt = os.getenv('KILL_EXEMPT', None)
start_exempt = os.getenv('START_EXEMPT', None)
min_containers = int(os.getenv('MIN_CONTAINERS', yml_config['min_containers']))
max_containers = int(os.getenv('MAX_CONTAINERS', yml_config['max_containers']))

run_time = os.getenv('RUN_TIME', yml_config['run_time'])

# Set up docker client
docker_api_version = str(os.getenv('DOCKER_API_VERSION', yml_config['docker_remote_api_version']))
docker_base_url = yml_config.get('base_url', None)
if docker_base_url is not None:
    docker_client = Client(base_url=docker_base_url,version=docker_api_version)
else:
    docker_client = Client(base_url='unix://var/run/docker.sock', version=docker_api_version)


if kill_exempt is None:
    kill_exempt = yml_config['kill']['exempt_containers']
else:
    kill_exempt =  kill_exempt.split(',')

if start_exempt is None:
    start_exempt = yml_config['start']['exempt_containers']
else:
    start_exempt =  start_exempt.split(',')

def get_containers(docker_client, exempt_containers, status):
    valid_containers = []
    for container in docker_client.containers(filters={'status':status}):
        valid = True
        for ex_cont in exempt_containers:
            if ex_cont in container['Names'] or ex_cont == container['Id']:
                valid = False
            ex_cont = '/' + ex_cont
            if ex_cont in container['Names'] or ex_cont == container['Id']:
                valid = False
        if valid:
            valid_containers.append(container['Id'])
    return valid_containers

def _start(interval,docker_client,max_containers,policy,exempt_containers,run_time):
    start_time = time.time()
    if run_time is None:
        run = True
        end_time = time.time() + 1
    else:
        run = False
        end_time = time.time() + (random.uniform(0, run_time) * 60)
    while(run or (time.time() < end_time)):
        containers = {}
        containers['running'] = get_containers(docker_client,exempt_containers,'running')
        containers['killed'] = get_containers(docker_client,exempt_containers,'exited')
        # print(containers)
        if len(containers['running']) < max_containers and len(containers['killed']) > 0:
            start_cont = random.choice(containers['killed'])
            print('starting container: ' + start_cont)
            containers['killed'].remove(start_cont)
            try:
                docker_client.start(start_cont)
                containers['running'].append(start_cont)
            except:
                print('could not start container %s' %(start_cont,))
        else:
            print('no containers available to start')
        time.sleep(random.uniform(0, start_interval))
    print('Start worker: %s Start: %s End: %s '%(os.getpid(),start_time,time.time()))
    return

def _kill(interval,docker_client,min_containers,policy,exempt_containers,run_time):
    start_time = time.time()
    if run_time is None:
        run = True
        end_time = time.time() + 1
    else:
        run = False
        end_time = time.time() + (random.uniform(0 , run_time) * 60)
    while(run or (time.time() < end_time)):
        containers = {}
        containers['running'] = get_containers(docker_client,exempt_containers,'running')
        containers['killed'] = get_containers(docker_client,exempt_containers,'exited')
        # print(containers)
        if len(containers['running']) > min_containers:
            kill_cont = random.choice(containers['running'])
            print('killing container: ' + kill_cont)
            containers['running'].remove(kill_cont)
            try:
                docker_client.kill(kill_cont)
                containers['killed'].append(kill_cont)
            except:
                print('could not kill container %s' %(kill_cont,))
        else:
            print('no containers available to kill')
        time.sleep(random.uniform(0, kill_interval))
    print('Kill worker: %s Start: %s End: %s '%(os.getpid(),start_time,time.time()))
    return

containers = {}

def stop():
    print('stop')
    #TODO:implement peaceful stop
    return


if __name__ == "__main__":
    print('Starting Chaos Monkey')
    print('INTERVAL \n start: %s kill %s' % (start_interval,kill_interval ))
    print('WORKERS \n start: %s kill %s' % (start_workers,kill_workers))
    print('MAX CONTAINERS: %s MIN CONTAINERS: %s ' % (max_containers,min_containers))
    print('RUN_TIME: %s' %(run_time,))
    policy = 'random'
    #Start workers
    # print('starting start workers')
    # print(containers)
    # _start(start_interval,docker_client,max_containers,policy,start_exempt,run_time,containers)
    # _kill(kill_interval,docker_client,min_containers,policy,kill_exempt,run_time,containers)
    processes = []
    for i in range(0,kill_workers):
        processes.append(multiprocessing.Process(target=_kill,args=(kill_interval,docker_client,min_containers,policy,kill_exempt,run_time)))
    for i in range(0,start_workers):
        processes.append(multiprocessing.Process(target=_start,args=(start_interval,docker_client,max_containers,policy,start_exempt,run_time)))
        
    for p in processes:
        p.start()
        time.sleep(random.uniform(0, ((start_interval+kill_interval)/2)))
    for p in processes:  
        p.join()
    print('Chaos Monkey Terminated')


