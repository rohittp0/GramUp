
# GramUp
## What is GramUp ?
**GramUp** is a lightweight python program to backup your files. **GramUp** enables you unlimited cloud backup and easy restore functionality and that too for free. With **GramUp** monthly bills for cloud storage will be a thing of the past. 
##  How dose it work ?
**GramUp** uses Telegram's unlimited cloud storage for backup. All your files are stored on Telegram servers and secured by their encryption. You can select a chat ( usually saved messages ) to use and **GramUp** will send all files to that chat and later at an event of restoration download files from there. Since both Telegram and **GramUp** are openscource you don't have to worry about someday suddenly you having to pay for your storage.
##  Key Features

 

 - [x]  **Unlimited Storage for Ever**
 
	 - Yes for ever ! That is not until a certain period of time or with a specific cap to the amount of storage you get. It is truly unlimited.
 - [x] **Fully Opensource**
 - [x]  **Works on any OS**
     - Anywhere you can run python or install Telegram **GramUp** will be avalable.
 - [x] **Unlimited Number of Device Support**
	 - Can run from any number or divices simultaniously ( both backup and restore )
 - [x] **Manual Upload and Download Support**
	 - Just send the file to Telegram and **GramUp** got you covered.
 - [x] **Preserves Directory Structure**
	 - **GramUp** remembers the relative path of your files so they can be recreated excactly when restoring.
 - [x] **Can Handle Any Kind of File**
	 - **GramUp** can backup and restore any type of file, let it be a image or a zip file **GramUp** can handle without any problem. 
 - [x] **Large File Size Support**
	 - **GramUp** supports file size of upto 1.5 GB ( will be increased in the next release )
 - [x] **Automatic File Tracking**
	 - **GramUp** checks the list of files already uploaded and uploads new files only to save you time and rescources.
 - [x] **Automatic Chat Identification**
	 - Just send 'use_this_chat' to any chat and **GramUp** will automatically select that chat for backup.
 - [x] **Easy setup**
	 - Whith easy 3 step guided setup process it is easier than you can imagine.
 - [x] **Light weight**
	 -  The whole program is just 35.7 kB I bet this must be the smallest app you have ever installed.

## Installation
**GramUp** currently provides two methods of installation, by cloning this repository or by using pip.

### Method 1 
The steps show is for linux, but can be easily replicated on other OS too, just google "cloning github repository from \<your OS\> "

Run the following commands from a terminal :

    git clone https://github.com/rohittp0/GramUp.git
    cd GramUp
    chmod +x run.sh    
	./run.sh

To run **GramUp** again open GramuUp/run.sh

### Method 2
This method always gets you the stable version of **GramUp** and is the recomended method. Install [pip](https://pypi.org/project/pip/) if you don't have it then run :

    pip install gramup
And that is it !

## Usage
### Windows
To start the program run,

     py -m gramup

 1. Then enter your phone number and list of folders you wan't to backup.
 2.  Now you will recive a code on your phone ( on Telegram ) enter that and press enter. 
 3. Now send "use_this_chat" to the Telegram chat you wan't to use for backup.
 4. Enter "b" for backup or "r" for retore.
 5. Now you can go out a have some fun while **GramUp** handles your task.
 ### Linux or MacOS
 The process is the same for you guys too. To start you can either run,
 

    python -m gramup
 or if you have your PATH configured just run, 
 

    gramup

   The rest is same as that for Windows

## Questions and Feedback

If you are facing any problem feel free to open an issue or mail me a stack overflow question with  `gramup`  as tag. Any and all pull requests are always welcome.

### Contact Me

**Mail me @**  [tprohit9@gmail.com](mailto:tprohit9@gmail.com)

**Catch me on**  [Stackoverflow](https://stackoverflow.com/users/10182024/rohi)

**Check out my YouTube**  [Channel](https://www.youtube.com/channel/UCVRdZwluF8jYXSIaHBqK73w)

**Follow me on**  [Instagram](https://www.instagram.com/rohit_pnr/)

     

 
