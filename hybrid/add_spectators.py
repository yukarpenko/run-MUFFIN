import numpy as np
import argparse
import os
import shutil

spectators = []  ## list of lists of spectators, in all events
spectator_events = 0  # number of initial-state configurations for hydro

def read_spectators():
 if os.path.exists(args.spectator_list):
  fspec = open(args.spectator_list, 'r')
 else:
  return None
 buff = []
 spectator_events = 0
 for line in fspec:
  if(len(line.split()) == 12):
   buff.append(line)
  if(line.startswith('#event')): # catches the # event X out Y lines
   if buff:
    #print(line)
    print('int. spectator count: ', spectator_events, '  mult ', len(buff))
    spectators.append(buff)
    spectator_events = spectator_events + 1
    buff = []


def compute_sampler_events():
 f = open(args.sampled_particle_list, 'r')
 sampled_events = 0
 for line in f:
  if(line.startswith('# event') and line.split()[3] == 'end'):
   sampled_events = sampled_events + 1
 return sampled_events

def read_sampler_output_and_write_full_output():
 f = open(args.sampled_particle_list, 'r')
 fout = open(args.output, 'w')
 buff = []
 event_count = 0
 spectator_event_count = 0
 max_id = 0
 for line in f:
  if(line.startswith('#!OSCAR2013') or line.startswith('# Units') or line.startswith('# SMASH')):
   fout.write(line)
  if(len(line.split()) == 12):
   buff.append(line)
   max_id = max(max_id, int(line.split()[10]))
  if(line.startswith('# event') and line.split()[3] == 'end'): # catches the # event X out Y lines
   print(line)
   print('int. event count: ', event_count, '  mult ', len(buff))
   print('max_id: ', max_id)
   fout.write('# event ' + str(event_count) + ' out ' + str(len(buff)+len(spectators[spectator_event_count])) + '\n')
   fout.write(''.join(buff))  ## write the sampled hadrons
   fout.write(''.join(spectators[spectator_event_count]))  ## add the spectators!
   fout.write('# event ' + str(event_count) + ' end 0 impact   0.000 scattering_projectile_target yes\n')
   event_count = event_count + 1
   spectator_event_count = spectator_event_count + 1
   if(spectator_event_count>spectator_events-1):
    spectator_event_count = 0
   buff = []
   max_id = 0


if __name__ == '__main__':
 parser = argparse.ArgumentParser()
 parser.add_argument("--sampled_particle_list", required = True,
                     help="File containing the sampled particle lists.")
 parser.add_argument("--spectator_list", required = True,
                     help="File containing the spectator lists.")
 parser.add_argument("--output", required = True,
                     help="output")
 args = parser.parse_args()
 
 read_spectators()
 sampler_events = compute_sampler_events()
 if(spectator_events>=sampler_events):
  print('add_spectators.py:  merging spectators and sampled hadrons...')
  read_sampler_output_and_write_full_output()
 else:
  print('add_spectators.py:  sampler events ', sampler_events, ' spectator events ',spectator_events)
  print('add_spectators.py:  passing sampled hadrons to output...')
  shutil.copy(args.sampled_particle_list, args.output)

 print('length of spectator meta-array: ', len(spectators))
 #print(spectators)
