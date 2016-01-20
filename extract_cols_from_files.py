# Author - Praveen Taneja
# last updated - 01/20/16

import glob
import wx
import os
#import sys
import csv
#import pandas as pd


fn_match = '*.csv'
#start_row = 12 # counting from 1
#col_num = 4# counting from 1


def choose_dir():
    app = wx.App()
    dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        folder_path = dialog.GetPath()
    dialog.Destroy()
    return folder_path

# from http://stackoverflow.com/questions/18532827/using-wxpython-to-get-input-from-user
def ask(parent=None, message=''):
        app = wx.App()
        dlg = wx.TextEntryDialog(parent,
                                  message)
        dlg.ShowModal()
        result = dlg.GetValue()
        
        dlg.Destroy()
        app.MainLoop()
         
        return result

def valid_user_input_float(x):
    # http://stackoverflow.com/questions/19157374/python-input-validation
    try:
        return float(x)
    except ValueError:        
        return False

folder_path = choose_dir()
folder_name = os.path.basename(folder_path)


col_num = ask(message = 'Enter column number (eg. 4)')
while valid_user_input_float(col_num) == False or col_num == 0:
    col_num = ask(message = 'Enter column number (eg. 4)')
col_num = int(col_num)

start_row = ask(message = 'Enter starting row number (eg. 12)')
while valid_user_input_float(start_row) == False or start_row == 0:
    start_row = ask(message = 'Enter starting row number (eg. 12)')
start_row = int(start_row)

print ' '
print 'extracting col #', col_num, ', starting from row #', start_row

start_row = start_row - 1
col_num = col_num -1
print ' '
print 'reading .csv files from folder', folder_path

fn_list = glob.glob(folder_path +'/'+ fn_match)
print ' '
print 'found files, n =', len(fn_list)

data = []

for fn in fn_list:
    data_file_w_ext = os.path.basename(fn)
    data_file_no_ext = os.path.splitext(data_file_w_ext)[0]
    
    row_vals = []
    row_vals.append(data_file_w_ext)
    with open(fn, 'rb') as csvfile:
        csvr = csv.reader(csvfile)
        for row_num, row in enumerate(csvr):
            if row_num >= start_row:
                #print row
                if len(row) -1 >= col_num:
                    row_vals.append(row[col_num])
                else: # if not enough cols in row 01/20/16
                    row_vals.append('')
                #print row_vals
                
        data.append(row_vals)
        #print data

results_dir = folder_path + '/results'
print ' '
print 'extracted in "results" subfolder'#, results_dir

if not os.path.exists(results_dir):
    os.makedirs(results_dir)
        
#out_fn = results_dir + '/' + folder_name + str(row_num + 1) + str(col_num + 1) + '.csv'
out_fn = results_dir + '/' + folder_name + '.csv'           
with open(out_fn, 'wb') as fh:
    csvw = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
    for row in data:
        csvw.writerow(row)

        
