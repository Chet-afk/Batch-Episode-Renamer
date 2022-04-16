import os


filePath = input("Please enter file path: ")


os.chdir(filePath)
cwd = os.getcwd()
print("Current Directory: ", cwd)

files = os.listdir(".")

for each_file in files:

    print(each_file)    # Done in a loop for nicer formatting
    os.rename(each_file, each_file[:-4] + each_file[-4:])   # Rename instead of Replace so program stops if it tries to replace itself

