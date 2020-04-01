# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 21:25:43 2020

@author: test
"""
#init libs
print("Please wait. Packages initialization...")
import csv
import numpy as np
from tensorflow.python.keras.models import model_from_json
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog


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



pte_adapted="PTE_adapted.txt"
model_json="network.json"
model_h5="network.h5"

min_temp=0
max_temp=999

defalut_result_name="/results.txt"
result_path="results.txt"
source_path="source.txt"
target_size=10#num of position for elements
num_elements=17# params of element in formula



class SupercoNN_class(QDialog):
    error_flag=False
    def __init__(self):
        super(SupercoNN_class, self).__init__()
        loadUi('GUI_window.ui', self)
        #init text fields
        self.setWindowTitle('SupercoNN')
        self.Source_file_lineEdit.setText(source_path)
        self.Result_path_lineEdit.setText(result_path)
        self.Min_temp_lineEdit.setText(str(min_temp))
        self.Max_temp_lineEdit.setText(str(max_temp))
        
        #init signals and slots
        self.Set_result_path.clicked.connect(self.set_result_directory_path)
        self.Set_source_file.clicked.connect(self.set_source_file_path)
        self.Start_btn.clicked.connect(self.Start_function)
    @pyqtSlot()
    
        
    def set_result_directory_path(self):
        result_path = str(QFileDialog.getExistingDirectory(self, "Select Directory for Result File"))
        if result_path!="":
            result_path=result_path+defalut_result_name
            self.Result_path_lineEdit.setText(result_path)
        
    def set_source_file_path(self):
        source_path = QFileDialog.getOpenFileName(self, "Select Source File", "", "Text Files (*.txt *.csv)")
        if source_path[0]!="":
            source_path=source_path[0]
            self.Source_file_lineEdit.setText(source_path)
        
    def Start_function(self):
        #init variables
        elements=[]
        formulas=[]
        fromulas_processed=[]
        nums_custom_formulas=0
        #----------------------------
        self.log_listWidget.addItem("--INFO-- Files checking")
        #set temperatures
        try:
            min_temp=float(self.Min_temp_lineEdit.text())
            if min_temp<0:
                self.error_flag=True
                self.log_listWidget.addItem("--ERROR-- Minimum temperature can not be smaller than 0")

        except ValueError:
            self.error_flag=True
            self.log_listWidget.addItem("--ERROR-- Minimum temperanure must be number")

        try:
            max_temp=float(self.Max_temp_lineEdit.text())
        except ValueError:
            self.error_flag=True
            self.log_listWidget.addItem("--ERROR-- Maximum temperanure must be number")
        #------------------------------------------------
        #read cemestry table file
        
        try:
            csv_chemestry_table=open(pte_adapted, newline='')
            reader_chemestry_table = csv.reader(csv_chemestry_table, delimiter=',', quotechar='|')
             #reading chemestry table    
            next(reader_chemestry_table)#drop headers
            for i in range(86):
                read_row = next(reader_chemestry_table)
                for j in range(len(read_row)):
                    read_row[j]=float(read_row[j])
                elements.append(read_row)
            csv_chemestry_table.close()
        except FileNotFoundError:
            self.error_flag=True
            self.log_listWidget.addItem("--ERROR-- Progam can not find file with chemestry table.")
            self.log_listWidget.addItem("--ERROR-- File PTE_adapted.txt must be in defalut folder.")
            self.log_listWidget.addItem("--ERROR-- Also you can download it from git:https://github.com/devdimit93/SupercoNN ")
        #---------------------------------------------
        #prepare result file

        try:
            result_path=str(self.Result_path_lineEdit.text())
            result_cs_writer=open(result_path, 'a', newline='')
            result_writer = csv.writer(result_cs_writer, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        except FileNotFoundError:
            self.error_flag=True
            self.log_listWidget.addItem("--ERROR-- Programm can not open path for result file.")
            self.log_listWidget.addItem("--ERROR-- Check path to result file")
        #--------------------------------------------------
        #reading and processing of source file
        try:
            source_path=str(self.Source_file_lineEdit.text())
            csv_custom=open(source_path, newline='')
            reader_custom = csv.reader(csv_custom, delimiter=',', quotechar='|')
            element_names=["H","He","Li","Be","B","C","N", "O","F", "Ne",
                   "Na","Mg","Al","Si","P","S", "Cl","Ar", 
                   "K","Ca","Sc","Ti","V","Cr","Mn","Fe", "Co","Ni", "Cu","Zn","Ga","Ge","As","Se","Br","Kr", 
                   "Rb","Sr", "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd", "Ag","Cd", "In","Sn","Sb","Te","I","Xe",
                   "Cs","Ba", "La",
                   "Ce", "Pr","Nd","Pm", "Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm", "Yb","Lu",
                   "Hf","Ta", "W","Re","Os","Ir","Pt","Au","Hg","Ti", "Pb","Bi", "Po","At","Rn"
                   ]
            rows=[]

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
            
            #formulas processing. stage2 
            #expansion formulas to size 10*17. 10*17 - size of neural network input. 
            #10 elements in formula, every element has 16 parametrs and 1 coefficient
            add_arr=[]# herea will be abstract element. all parametrs of its is zero
            for i in range(num_elements):
                add_arr.append(0)
            add_arr=np.asarray(add_arr)


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
            csv_custom.close()
        except FileNotFoundError:
            self.error_flag=True
            self.log_listWidget.addItem("--ERROR-- Programm can not find source file.")
            self.log_listWidget.addItem("--ERROR-- Check path to source file.")
        #--------------------------------------------------------
        #prepare model. reading model files
        
        try:
            self.log_listWidget.addItem("--INFO-- Reading model files. Please wait some time")
            json_file = open(model_json, "r")
            loaded_model_json = json_file.read()
            json_file.close()
            model = model_from_json(loaded_model_json)
        except FileNotFoundError:
            self.error_flag=True
            self.log_listWidget.addItem("--ERROR-- Progam can not find json file of the pretrained model ")
            self.log_listWidget.addItem("--ERROR-- You can download this file from git:https://github.com/devdimit93/SupercoNN/pretrained_nn")
            self.log_listWidget.addItem("--ERROR-- Rename downloaded file into network.json ")
        
        try:
             model.load_weights(model_h5)
        except OSError:
            self.error_flag=True
            self.log_listWidget.addItem("--ERROR-- Progam can not find h5 file of the pretrained model")
            self.log_listWidget.addItem("--ERROR-- You can download this file from git:https://github.com/devdimit93/SupercoNN/pretrained_nn")
            self.log_listWidget.addItem("--ERROR-- Rename downloaded file into network.h5")
        #-------------------------------------------------------
        #prediction
        
        if self.error_flag==False:
            
            self.log_listWidget.addItem("--INFO-- All files are ready")

            self.log_listWidget.addItem("--INFO-- Start calculation")

            write_it_into_file=True# if True results will be writed into processed_data/results.txt . File will not be cleaned
            predicted = model.predict(fromulas_processed)
           
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
            
            
        if self.error_flag==True:
            self.log_listWidget.addItem("--ERROR-- Calculation was stopped")
        else:
            self.log_listWidget.addItem("--SUCСESSFUL-- Calculation was successfuly completed")
            self.log_listWidget.addItem("--SUCСESSFUL-- Results are in file: "+result_path)
        self.log_listWidget.addItem("---------------------------------")
app=QApplication(sys.argv)
widget=SupercoNN_class()
widget.show()
sys.exit(app.exec_())
        
        


