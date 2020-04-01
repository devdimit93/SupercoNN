# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 22:12:10 2020

@author: test
"""
import sys
#init libs
import csv
import numpy as np
from tensorflow.python.keras.models import model_from_json


#this function separate text and numbers(int and float)
def seperate_string_number(string):
    previous_character = string[0]
    groups = []
    newword = string[0]
    for x, i in enumerate(string[1:]):
        if i.isalpha() and previous_character.isalpha():
            newword += i
        elif i.isnumeric() and previous_character.isnumeric():
            newword += i
        else:
            groups.append(newword)
            newword = i

        previous_character = i

        if x == len(string) - 2:
            groups.append(newword)
            newword = ''
    buf=[]       
    next_idx=0
    for i in range(len(groups)):
        if i<len(groups)-1:
            if next_idx==i and groups[i+1]!=".":
                buf.append(groups[i])
                next_idx=next_idx+1
            if next_idx==i and  groups[i+1]==".":
                b_str=groups[i]+groups[i+1]+groups[i+2]
                buf.append(b_str)
                next_idx=i+3
        if i==len(groups)-1:
            if groups[i-1]!=".":
                buf.append(groups[i])        
    return buf

def main():
    data_path="source.txt"
    processed_data_path="results.txt"
    pte_adapted="PTE_adapted.txt"
    model_json="network.json"
    model_h5="network.h5"
    min_temp=0
    max_temp=999
    cleaner=False
    for i in range(len (sys.argv)):
        my_index = str(sys.argv[i]).find('sp:') 
        if(my_index==0):
            data_path=str(sys.argv[i])[3:]
        my_index = str(sys.argv[i]).find('tp:') 
        if(my_index==0):
            processed_data_path=str(sys.argv[i])[3:]
        my_index = str(sys.argv[i]).find('mint:') 
        if(my_index==0):
            min_temp=str(sys.argv[i])[5:]
            min_temp=float(min_temp)
        my_index = str(sys.argv[i]).find('maxt:') 
        if(my_index==0):
            max_temp=str(sys.argv[i])[5:]
            max_temp=float(max_temp)
        my_index = str(sys.argv[i]).find('clear') 
        if(my_index==0):
            cleaner=True
    if(data_path=="source.txt"):
        print("--WARNING-- Defalut data path is used")
    if(processed_data_path=="results.txt"):
        print("--WARNING-- Defalut path for results is used")
        
    if(min_temp==0):
        print("--WARNING-- Defalut minimum temperature filter is used. minimum temperature=0")
    if(max_temp==999):
        print("--WARNING-- Defalut maximum temperature filter is used. maximum temperature=999")
        
    #cleaning
    # opening the file with w+ mode truncates the file
    if cleaner==True:
        f = open(processed_data_path, "w+")
        f.close()
        print("--INFO-- file "+processed_data_path+ " was cleaned")
    
#################################################################
    #file with formulas
    try:
        csv_custom=open(data_path, newline='')
        reader_custom = csv.reader(csv_custom, delimiter=',', quotechar='|')
    except FileNotFoundError:
        print("--ERROR-- Progam can not find file with formulas. Check path to file or use file Source.txt in defalut folder.\n Path must be like E:\data\source.txt")
        sys.exit()
    #adapted periodic table for neural network (DO NOT CHANGE IT)
    try:
        csv_chemestry_table=open(pte_adapted, newline='')
        reader_chemestry_table = csv.reader(csv_chemestry_table, delimiter=',', quotechar='|')
    except FileNotFoundError:
        print("--ERROR-- Progam can not find file with chemestry table. File PTE_adapted.txt must be in defalut folder. Also you can download it from git:https://github.com/devdimit93/SupercoNN ")
        sys.exit()

    #
    target_size=10#num of position for elements
    num_elements=17# params of element in formula
 ######################################################################
    
    #reading rows from txt files
    #reading formulas
    rows=[]
    nums_custom_formulas=0
    read_it=True

    while(read_it==True):
        try:
            read_row = next(reader_custom)
            rows.append(read_row)
            nums_custom_formulas=nums_custom_formulas+1
        except StopIteration:
            read_it=False
    processed_rows=[]
    for i in range(len(rows)):
        buf=seperate_string_number(rows[i][0])
        processed_rows.append(buf)
                
    #reading chemestry table    
    next(reader_chemestry_table)#drop headers
    elements=[]
    for i in range(86):
        read_row = next(reader_chemestry_table)
        for j in range(len(read_row)):
            read_row[j]=float(read_row[j])
        elements.append(read_row)
##############################################################

    #order of elements
    element_names=["H","He","Li","Be","B","C","N", "O","F", "Ne",
                   "Na","Mg","Al","Si","P","S", "Cl","Ar", 
                   "K","Ca","Sc","Ti","V","Cr","Mn","Fe", "Co","Ni", "Cu","Zn","Ga","Ge","As","Se","Br","Kr", 
                   "Rb","Sr", "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd", "Ag","Cd", "In","Sn","Sb","Te","I","Xe",
                   "Cs","Ba", "La",
                   "Ce", "Pr","Nd","Pm", "Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm", "Yb","Lu",
                   "Hf","Ta", "W","Re","Os","Ir","Pt","Au","Hg","Ti", "Pb","Bi", "Po","At","Rn"
                   ]
    #formulas processing. stage1
    #transform formulas from text to set of parametrs
    formulas=[]
    for i in range(len(processed_rows)):#formulas
        elem_buf=[]
        order=[]
        for j in range(len(processed_rows[i])):#elements
            
            for k in range(len(element_names)):#parametrs
                if processed_rows[i][j]==element_names[k]:
                    order.append(k)
                    buf=[]
                    if j!=len(processed_rows[i])-1:
                        buf.append(float(processed_rows[i][j+1]))#coefficient
                    else:
                        buf.append(float(1))#
                    for f in range(len(elements[85])):
                        buf.append(float(elements[k][f]))
                    buf=np.asarray(buf)
                    elem_buf.append(buf)
        #sort by atomic number
        sorted_elem_buf=[]
        for i in range(len(order)):
            min_index = order.index(min(order))
            sorted_elem_buf.append(elem_buf[min_index])
            order[min_index]=999
        sorted_elem_buf=np.asarray(sorted_elem_buf)
        formulas.append(sorted_elem_buf)#elem_buf is transformed formula
    formulas=np.asarray(formulas)
##########################################################
    #formulas processing. stage2 
    #expansion formulas to size 10*17. 10*17 - size of neural network input. 
    #10 elements in formula, every element has 16 parametrs and 1 coefficient
    add_arr=[]# herea will be abstract element. all parametrs of its is zero
    for i in range(num_elements):
        add_arr.append(0)
    add_arr=np.asarray(add_arr)


    fromulas_processed=[]
    for i in range(formulas.shape[0]):
        dist=target_size-formulas[i].shape[0]
        buf1=[]
    
        if dist>0:
            for j in range(dist):
                buf1.append(add_arr)
        for j in range(formulas[i].shape[0]):
            buf1.append(formulas[i][j])
        buf1=np.asarray(buf1)
        fromulas_processed.append(buf1)    
    fromulas_processed=np.asarray(fromulas_processed)
############################################################
    try:
        json_file = open(model_json, "r")
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
    except FileNotFoundError:
        print("--ERROR-- Progam can not find json file of the pretrained model. You can download this file from git:https://github.com/devdimit93/SupercoNN/pretrained_nn . Rename downloaded file into network.json ")
        sys.exit()
    
   
    
    

    try:
        model.load_weights(model_h5)
    except OSError:
        print("--ERROR-- Progam can not find h5 file of the pretrained model. You can download this file from git:https://github.com/devdimit93/SupercoNN/pretrained_nn . Rename downloaded file into network.h5 ")
        sys.exit()

    print("--INFO-- Neural network ready. Start calculation")

############################################################
#you can select results with different temperatures


    #here wiil be results
    write_it_into_file=True# if True results will be writed into processed_data/result.txt . File will not be cleaned



    predicted = model.predict(fromulas_processed)
    result_cs_writer=open(processed_data_path, 'a', newline='')
    result_writer = csv.writer(result_cs_writer, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    if write_it_into_file==False:
        result_cs_writer.close() 
    results=[]
    counter=0
    for i in range(nums_custom_formulas):
        if predicted[i][0]<max_temp and predicted[i][0]>min_temp:
            buf=[]
            buf.append(rows[i][0])
            buf.append(str(predicted[i][0]))
            results.append(buf)
            counter=counter+1        
    header=[]
    result_writer.writerow(header)
    result_cs_writer.flush()    
    header.append("formula")
    header.append("critical_temperature")
    result_writer.writerow(header)
    result_cs_writer.flush()    
    if write_it_into_file==True:
        for i in range(counter):
            result_writer.writerow(results[i])
            result_cs_writer.flush()
    
        result_cs_writer.close()
if __name__== "__main__":
  main()
  print("--INFO-- Calculation successfully completed")