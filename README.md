
# GramUp

  1. [What is GramUp?](#what-is-gramup-)
  2. [How does it work?](#how-does-it-work-)
  3. [Key Features](#key-features)
  4. [Installation](#installation)
		* [Method 1](#method-1)
	    * [Method 2](#method-2)
  5. [Usage](#usage)
	    * [Windows](#windows)
	    * [Linux or MacOS](#linux-or-macos)
  6. [Questions and Feedback](#questions-and-feedback)
	    * [Contact Me](#contact-me)

## What is GramUp?

**GramUp** is a lightweight python program to backup your files. **GramUp** enables you unlimited cloud backup and easy restore functionality and that too for free. With **GramUp,** monthly bills for cloud storage will be a thing of the past. 

##  How does it work?

**GramUp** uses Telegram's unlimited cloud storage for backup. All your files are stored on Telegram servers and secured by their encryption. You can select a chat ( usually saved messages ) to use and **GramUp** will send all files to that chat and later at an event of restoration download files from there. Since both Telegram and **GramUp** are opensource you don't have to worry about someday suddenly you having to pay for your storage.

##  Key Features

 - [x]  **Unlimited Storage for Ever**
	 - Yes forever! That is not until a certain period of time or with a specific cap to the amount of storage you get. It is truly unlimited.
 - [x] **Fully Opensource**
 - [x]  **Works on any OS**
     - Anywhere you can run python or install Telegram **GramUp** will be available.
 - [x] **Unlimited Number of Device Support**
	 - Can run from any number of devices simultaneously ( both backup and restore )
 - [x] **Manual Upload and Download Support**
	 - Just send the file to Telegram and **GramUp** got you covered.
 - [x] **Preserves Directory Structure**
	 - **GramUp** remembers the relative path of your files so they can be recreated exactly when restoring.
 - [x] **Can Handle Any Kind of File**
	 - **GramUp** can backup and restore any type of file, let it be an image or a zip file **GramUp** can handle without any problem. 
 - [x] **Large File Size Support**
	 - **GramUp** supports file size of up to 1.5 GB ( will be increased in the next release )
 - [x] **Resumable Backup and Restore**
	 - **GramUp** checks the list of files already uploaded/downloaded and uploads/downloads new files only to save you time and resources.
 - [x] **Automatic Chat Identification**
	 - Just send 'use_this_chat' to any chat and **GramUp** will automatically select that chat for backup.
 - [x] **Easy setup**
	 - With easy 3 steps guided setup process, it is easier than you can imagine.
 - [x] **Light weight**
	 -  The whole program is just 35.7 kB I bet this must be the smallest app you have ever installed.

## Installation

**GramUp** currently provides two methods of installation, by using pip or by cloning this repository.

### Method 1

This method always gets you the stable version of **GramUp** and is the recommended method. Install [pip](https://pypi.org/project/pip/) if you don't have it then run :

    pip install gramup
And that is it!

### Method 2 

This method ensures that you get the latest version ( even if it is unstable ).
The steps shown are for Linux but can be easily replicated on other OS too, just google "cloning GitHub repository from \<your OS\> "

Run the following commands from a terminal :

    git clone https://github.com/rohittp0/GramUp.git
    cd GramUp
    chmod +x run.sh    
	./run.sh

To run **GramUp** again open GramuUp/run.sh


## Usage

### Windows

To start the program run,

     py -m gramup

 1. Then enter your phone number and list of folders you want to backup.
 2. Now you will receive a code on your phone ( on Telegram ) enter that and press enter. 
 3. Now send "use_this_chat" to the Telegram chat you want to use for backup.
 4. Enter "b" for backup or "r" for retore.
 5. Now you can go out a have some fun while **GramUp** handles your task.
 
### Linux or MacOS
 
 The process is the same for you guys too. To start you can either run,
 

    python -m gramup
 or if you have your PATH configured just run, 
 

    gramup

   The rest is the same as that for Windows

### Adroid/iOS

 Currently **GramUp** doesn't support automatic backup and restore on Android/iOS. You could backup files manually by sending them to the chat you selected for backup ( must be sent as document ) with the path to where you want it restored as the caption.

Files backed up by **GramUp** can be accessed using the UnLim app on Android. [UnLim](https://play.google.com/store/apps/details?id=com.kratosle.unlim&hl=en_IN&gl=US) can also be used to backup files from Android to then be restored using **GramUp**. To make **GramUp** compatible with UnLim just select the "saved messages" chat ( The chat which is used by UnLim ) as the chat for backup. Do check out UnLim's [facebook page](https://www.facebook.com/unlimcloudteam/).
  

## Questions and Feedback

If you are facing any problem feel free to open an issue or mail me a stack overflow question with  `gramup`  as the tag. All pull requests are always welcome.

### Contact Me

**Mail me @**  [tprohit9@gmail.com](mailto:tprohit9@gmail.com)

**Catch me on**  [Stackoverflow](https://stackoverflow.com/users/10182024/rohi)

**Check out my YouTube**  [Channel](https://www.youtube.com/channel/UCVRdZwluF8jYXSIaHBqK73w)

**Follow me on**  [Instagram](https://www.instagram.com/rohit_pnr/)

     

 
