import os

def main():
    
    
    filePath = input("Please enter file path: ")


    os.chdir(filePath)
    cwd = os.getcwd()
    
    print("\nCurrent Directory: " + cwd + "\n")

    files = os.listdir(".")

    
    renamed = input("What would you like to rename the files to?: ").strip()
    fileType = input("What is the file extension? (i.e .mkv, .mp4): ").strip()
    epNum = 1
    
    for each_file in files:
        
        if os.path.isdir(each_file):
            
            print("\"" + each_file + "\"", "is a directory.")
            
            continue
        
        print("\n" + each_file , "is being renamed to: " + renamed + " Episode " + str(epNum) + fileType)    # Done in a loop for nicer formatting
        
        os.rename(each_file, renamed + " Episode " + str(epNum) + fileType)   # Rename instead of Replace so program stops if it tries to replace itself
        epNum += 1


main()
