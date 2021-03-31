import os 
import shutil

def manage_zip_upload(instance, tempDir, targetDir) :
  for mainDir, subdirs, files in os.walk(tempDir) :

        for file in files :
            ext = os.path.splitext(file)[1]
            if ext == '.html' :
                print('File :',file)
                print('Main Directory :', mainDir)
                print('Dirs in current directory :', subdirs)
                os.rename(os.path.join(mainDir, file), os.path.join(mainDir, 'index.html'))
                #mainDir_name = os.path.split(mainDir)[-1]
                new_mainDir = os.path.join(os.path.dirname(mainDir), instance.name)
                try :
                    os.rename(mainDir, new_mainDir)
                except FileExistsError :
                    pass
                except Exception as error :
                    print(error)
                
                try :
                    shutil.move(new_mainDir, targetDir)
                except Exception as error:
                    print(error)

                shutil.rmtree(tempDir, ignore_errors=True)