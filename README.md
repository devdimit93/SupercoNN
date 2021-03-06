# SupercoNN
SupercoNN is project for the prediction of the temperature of superconductivity of materials based on a chemical formula by neural network.
--------------------------------------------
- In this project were used:
- Tensorflow 1.15.0
- Matplotlib 3.1.1
- NumPy 1.18.1
- Superconductivty Data Data Set - open dataset, containing superconductors chemistry formulas. https://archive.ics.uci.edu/ml/datasets/Superconductivty+Data

------------------------------------------------
Metrics of trained neural network for defalut test dataset:
- Root mean square error, RMSE 8.202
- Standard deviation, R2 0.923
- Mean absolute error, MAE 4.068
It mean that neural network can predict critical temperature of superconductivity of chemistry formula with accuracy 4.068 degree

------------------------------------------
How can you run and train this network:

1. Start prediction for your formulas

1.1 Put txt file with your chemistry formulas into folder “processed_data”. Structure of formulas must be as in file "formulas_example.txt". Order of elements in formula is not important for this version of neural network

1.2 Run "work_with_custom_formulas_pretrained_network.ipynb" file. In this file find variable "csv_custom" and insert there path to your file with formulas

1.3 If you want write results into file, change path to this file in variable "result_cs_writer" and set variable "write_it_into_file" True.  If you don’t want write results, set False

1.4 Run all cells in this ipynb file. 

2. Training process

2.1 (optional)Start file "parserBIG.ipynb". 
This file makes dataset processing for training process.
Processed data already is in folder "processed_data" in files "train_dataset.txt" and "test_dataset.txt"
This repository has not default dataset in this folder. 
You can download test dataset by link https://drive.google.com/open?id=1h-le5YqJKfOXUPhDARZxCq_D8qGT0BzJ
You can download train dataset by link https://drive.google.com/open?id=1jiiHWyCiTJSE6kwET9biYVn4FkbiI6XY
Put these datasets in folder "processed_data".
If you want crate your own dataset, you must remove default dataset.

2.2 Start training of different networks with different structure by files: 
- lstm_trainer.ipynb
- convolution_C1_trainer.ipynb
- convolution_C2_trainer.ipynb
- convolution_C3_trainer.ipynb

These files use loss "Mean Absolute Error"(MAE)
Pretrained models will be in folder "pretrained_data". 
This repository already has default pretrained models for default dataset 

2.3 Optimize pretrained networks for “Mean Square Error”(MSE) loss by file “mse_optimiser.ipynb” . In variables “model2j” and “model2h” show path to .json and .h5 files of pretrained model. In variable “json_file” and function “model.save_weights” show path , where optimized model will be saved.

2.4 Make ensemble of C2 and C3 networks by file “Ensemble_C2_C3_trainer.ipynb”. After training this network must be adapted for  MSE loss too.

2.5 All models were trained. Start file “Best_ensemble.ipynb”. In this file best ensemble will be created. Trained ensemble of neural network will be saved in folder “pretrained_nn”.

2.6 Test it for custom formulas. See p.1.

In folder Console_supercoNN and GUI_SupercoNN you can see python scripts for application. 

These scripts need tensorflow, numpy and python. 

Compiled applications are available via Google Drive links at the end of this description. 
They can work without python and other packages. 
They was tested on the Windwos 7 and 10.

Console_supercoNN - console version of script. You can launch it by command like 
python main.py sp:E:\data\source.txt tp:E:\results.txt mint:20 maxt:87 clean
 - sp: - path to source file with chemistry formulas. Defalut value "results.txt", file in this folder.
 - tp: - path to file, where will be calculated results.
 If file does not exist, it will be created. Results has format: formula from source file, critical temperature. Defalut value "results.txt", file in this folder 
 - mint: - minimum critical temperature.
 Of predicted critical temperature of chemestry formula is smaller than value mint, formula will not be writed into results file from tp: parametr. Defalut walue 0 
 - maxt: - maximum critical temperature. 
 If predicted critical temperature of chemestry formula is more than value maxt, formula will not be writed into results file from tp: parametr. Defalut walue 999 
 - clean - cleaning results file. 
 If you use this parametr, file from parametr tp: will be cleaned before calculation. If you dont use this parametrs, results will be added in the end of file.

GUI_SupercoNN - graphical user interface script. For this script work, you need to install pyqt5 and pqt5-tools.

If you need more information, you can see it inside .ipynb files in comments. 

-----------------------------------------------------------------
Link to Google Drive the compressed archive with source code  https://drive.google.com/open?id=1kxzH1UuanuGdupbfQ64dqcrO0VnEP3eM.

Link to Google Drive the archive with compiled console application  https://drive.google.com/open?id=1rLvQ68HN7wLm-HSBInnW14MobtNOBVD6

Link to Google Drive the archive with compiled GUI application  https://drive.google.com/open?id=1tpb-hLHW_UFco0kCekYXcqg4YGlz0it4
