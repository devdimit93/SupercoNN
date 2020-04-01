If you use windows console for starting programm you can use command with some parametrs: launcher.exe sp:E:\data\source.txt tp:E:\results.txt mint:20 maxt:87 clean
List of parametrs: sp: - path to source file with chemistry formulas. Defalut value "results.txt", file in this folder.
 tp: - path to file, where will be calculated results.
 If file does not exist, it will be created. Results has format: formula from source file, critical temperature. Defalut value "results.txt", file in this folder 
 mint: - minimum critical temperature.
 Of predicted critical temperature of chemestry formula is smaller than value mint, formula will not be writed into results file from tp: parametr. Defalut walue 0 
 maxt: - maximum critical temperature. 
 If predicted critical temperature of chemestry formula is more than value maxt, formula will not be writed into results file from tp: parametr. Defalut walue 999 
 clean - cleaning results file. 
 If you use this parametr, file from parametr tp: will be cleaned before calculation. If you dont use this parametrs, results will be added in the end of file.
------------------------------------------------
If you just start "launcher.exe" just from windows explorer, parametrs will have defalut values.
Formulas will be collected from file "source.txt".
Results of calculation will not be filtered by temperature parametrs.
Results will be saved into file "results.txt"
------------------------------------------------------
Formula limits for prediction model: If formula has some of this elements: He, Ne, Ar, Kr, Xe, Pm, Po, At, Rn, results can be incorrect. 
Model was not trained for this elements.