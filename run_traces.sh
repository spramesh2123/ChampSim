#!/bin/bash
## This is the list of prefetchers we are testing ##
Prefetchers=('EIP'  'EIP_CB3_1' 'EIP_CB3_2' 'EIP_CB4_1' 'EIP_BB5' 'EIP_BB9' 'EIP_BB11' 'EIP_W8' 'EIP_W16' 'EIP_W48' 'EIP_W64' 'pips_S11' 'pips' 'pips_S8' 'pips_1SC' 'pips_2SC' 'pips_8SC' 'pips_4PQ' 'pips_5PQ' 'pips_6PQ' 'pips_8PQ' 'pips_9PQ' 'pips_10PQ' )
##Prefetchers=('pips' )
##Prefetchers=('D_JOLT' 'EIP' 'fnl_mma' 'mana' 'pips' 'tap')
## Building all the prefetchers ##
for i in {0..1}; do 
  printf "Building with prefetcher ${Prefetchers[i]}\n"
  printf "./build_champsim.sh hashed_perceptron ${Prefetchers[i]} next_line spp_dev no lru 1\n"
  ./build_champsim.sh hashed_perceptron ${Prefetchers[i]} next_line spp_dev no lru 1

  binary="hashed_perceptron-${Prefetchers[i]}-next_line-no-no-lru-1core"
  
  printf "##############${binary}###################\n"
  date +"%T"
  printf $"\n\n ------------ Running all the traces for ${i#*/} ------------\n\n"
    for j in ipc1_public/*; do
    printf "\n \t ./run_champsim.sh  ${binary} 50 50 ${j#*/}\n"
    ./run_champsim.sh ${binary} 50 50 ${j#*/} 
  done
  wait
done
