import glob
import re
import numpy as np
from statistics import geometric_mean as gm
import csv


rx_dict = {
    'IPC': re.compile(r'CPU\s*0\s*cumulative\s*IPC\D*(?P<IPC>\S*)'),
    'load_miss': re.compile(r'L1I.*LOAD.*MISS\D*(?P<load_miss>\S*)'),
    'l1_hit': re.compile(r'L1I.*LOAD.*HIT\D*(?P<l1_hit>\S*)'),
    'miss_latency': re.compile(r'L1I.*LATENCY\D*(?P<miss_latency>\S*)'),
    'useful': re.compile(r'L1I.*USEFUL\D*(?P<useful>\S*)'),
    'useless': re.compile(r'L1I.*USELESS\D*(?P<useless>\S*)'),

}
#model_list=['no','EIP','pips', 'EIP_W8','pips_S8', 'EIP_W64','pips_S11']
model_list=['no','EIP','EIP_BB3', 'EIP_BB5', 'EIP_BB9', 'EIP_BB11','pips','pips_1SC','pips_2SC','pips_8SC','pips_4PQ','pips_5PQ','pips_6PQ','pips_8PQ','pips_9PQ','pips_10PQ','tap','mana','pips_S11', 'pips_S8', 'EIP_W8', 'EIP_W64', 'EIP_CB3_1','EIP_CB3_2']
#model_list=['no','EIP','EIP_BB3', 'EIP_BB5', 'EIP_BB9', 'EIP_BB11', 'EIP_CB3_1','EIP_CB3_2']

all_result_dict = {}

for model in model_list:
    file_list = glob.glob(f"data_dump/*{model}-next*")
    #print(file_list)

    for filepath in file_list:
        result_dict = {}
        
        trace_tag = re.match(r'.*/(\S*).champ.*',filepath).group(1)
      #  print(trace_tag)
        with open(filepath,'r') as file:
            line = file.readline()
            while line:
                line = file.readline()

                for key,rx in rx_dict.items():
                    match = rx.match(line)
                    if match: 
                        result_dict[key] = float(match.group(key))
        if  trace_tag not in all_result_dict.keys(): all_result_dict[trace_tag] = {}
        all_result_dict[trace_tag][model] = result_dict

print(all_result_dict['client_001'])

    #print(all_result_dict)
# IPC_SPEED =  np.zeros((50,2))   
# for index, trace in enumerate(all_result_dict.keys()) : 
#     #print(f"Fisrst{all_result_dict[trace][model_list[0]]['IPC']} & Secomd {all_result_dict[trace][model_list[1]]['IPC']} Result: {IPC_SPEED[trace]} \n")
#     IPC_SPEED[index][0] = (all_result_dict[trace][model_list[1]]['IPC']/all_result_dict[trace][model_list[0]]['IPC'] - 1)*100
#     IPC_SPEED[index][1] = (all_result_dict[trace][model_list[2]]['IPC']/all_result_dict[trace][model_list[0]]['IPC'] - 1)*100
# print(gm(IPC_SPEED[0]))

# IPC_SPEED =  np.zeros((50,len(model_list)))   
# MISS_LATENCY = np.zeros((50,len(model_list)))
# L1I_MISS = np.zeros((50,len(model_list)))
# ACCURACY = np.zeros((50,len(model_list)))
# trace_list = []
# for index, trace in enumerate(all_result_dict.keys()) : 
#     #print(f"Fisrst{all_result_dict[trace][model_list[0]]['IPC']} & Secomd {all_result_dict[trace][model_list[1]]['IPC']} Result: {IPC_SPEED[trace]} \n")
#     for iter,test1 in enumerate(model_list) :
#         IPC_SPEED[index][iter] = (((all_result_dict[trace][test1]['IPC'])/all_result_dict[trace][model_list[0]]['IPC']))
#         MISS_LATENCY[index] = (all_result_dict[trace][test1]['miss_latency'])
#         L1I_MISS[index][iter] = (all_result_dict[trace][test1]['load_miss'])
#         ACCURACY[index][iter] = (all_result_dict[trace][test1]['useful']/(0.00001 + all_result_dict[trace][test1]['useful'] + all_result_dict[trace][test1]['useless']) )*100
#     trace_list.append(trace)



IPC_SPEED =  np.zeros((len(model_list),50))   
MISS_LATENCY = np.zeros((len(model_list),50))
L1I_MISS = np.zeros((len(model_list),50))
L1I_HIT = np.zeros((len(model_list),50))
HIT_RATE = np.zeros((len(model_list),50))
ACCURACY = np.zeros((len(model_list),50))
trace_list = []
for index, trace in enumerate(all_result_dict.keys()) : 
    #print(f"Fisrst{all_result_dict[trace][model_list[0]]['IPC']} & Secomd {all_result_dict[trace][model_list[1]]['IPC']} Result: {IPC_SPEED[trace]} \n")
    for iter,test1 in enumerate(model_list) :
        IPC_SPEED[iter][index] = ((all_result_dict[trace][test1]['IPC'])/all_result_dict[trace][model_list[0]]['IPC'])
        if IPC_SPEED[iter][index] < 0 : IPC_SPEED[iter][index] = 0.0000001
        MISS_LATENCY[iter][index] = (all_result_dict[trace][test1]['miss_latency'])#/all_result_dict[trace][model_list[0]]['load_miss'] - 1)*100
        L1I_MISS[iter][index] = (all_result_dict[trace][test1]['load_miss'])#/all_result_dict[trace][model_list[0]]['load_miss'] - 1)*100
        L1I_HIT[iter][index] = (all_result_dict[trace][test1]['l1_hit'])#/all_result_dict[trace][model_list[0]]['load_miss'] - 1)*100
        HIT_RATE[iter][index] = L1I_HIT[iter][index]/(L1I_HIT[iter][index] + L1I_MISS[iter][index])
        ACCURACY[iter][index] = (all_result_dict[trace][test1]['useful']/(0.00001 + all_result_dict[trace][test1]['useful'] + all_result_dict[trace][test1]['useless']) )*100

    trace_list.append(trace)
gmean_list = np.zeros((len(model_list),4))
for iter,test2 in enumerate(model_list) :
     if iter != 0:
        print(f"Model {test2} , IPC :{gm(IPC_SPEED[iter])}  MISS_LATENCY :{gm(MISS_LATENCY[iter])}  L1I_MISS :{gm(L1I_MISS[iter])} HIT_RATE :{gm(HIT_RATE[iter])}  ACCURACY :{gm(ACCURACY[iter])}  \n") 
        gmean_list[iter] = [gm(IPC_SPEED[iter]),gm(MISS_LATENCY[iter]),gm(HIT_RATE[iter]),gm(ACCURACY[iter])]

# print(gmean_list)
filename = "hw.csv"
# #print(MISS_LATENCY)    
# #writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(model_list) 
        
    # writing the data rows 
    csvwriter.writerows(gmean_list)

# textfile = open("a_file.txt", "w")
# for element in trace_list:
#     textfile.write(element + "\n")
# textfile.close()
