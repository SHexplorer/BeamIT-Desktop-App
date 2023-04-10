# BeamIT-Desktop-Application

This application was created as part of the university lecture "Software Engineering 2" as an exam. It is intended for sharing files, links and text. There are two repositorys for this project, the BeamIT-Desktop-Application and the BeamIT-Server (see [Beamit-Server](https://github.com/SHexplorer/BeamIT-Server))

The BeamIT-Desktop-Application is based on python 3.10+ and the QT-Framework. To run this app you need to install either the windows-setup or the appimage for linux. The windows-setup was created with Inno Setup and Winpython (see BeamIT-Desktop-Install.iss for setup recipe), the linux appimage was build with github actions and app-image-builder (see .github/build-appimage.yml and AppImageBuilder.yml). Requirement for this project was also some automated tests with github actions, so some small tests were implemented (see .github/module-test_and_syntax.yml and test_config.py). To run it from source you need python 3.10+ installed and following packages:

- PySide6
- webbrowser
- pyperclip

The code is more or less commented, just look a little bit around. The following part is a short usage manual (translated from german):
  

First you have to log in/register. In order to send a file, a URL link or a "simple" text, the desired receiving device must first be selected by clicking on it. Then the desired medium can be dragged and dropped into the designated field. It will be sent directly to the recipient. The recipient can set in his application whether incoming files should be opened directly or not. URL links are always opened directly in the browser set by the operating system. "Simple" text is automatically copied to the clipboard. The incoming files are also saved. This location can be customized using the "Set download path" button. By default this is set to C:/Users/.../Documents/BeamIT. The button "Locate files in explorer" calls the set path to display the files that were received.

Further the own device name can be adapted. By default, the device name of the operating system is used here. By deleting a device, the user is automatically logged out of the device. It is also possible to delete the entire account, or to log out of the device.


Quick guide:

1. login/registration
    
2. select receiving device
    
3. drag & drop files, URL links or "simple" text into the given field.
	 - Files can be opened automatically on the receiving device; URL links are always opened automatically; "simple" text is saved to the clipboard
    

4. If desired → make settings:
	- Files should be opened automatically
	- Adjust path where files should be saved
	- Rename own device