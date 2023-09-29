# Successor Product Finder (*Release Only*)

**Enter obsolete materials to receive a successor.**

## For B&R Employees
Source Code Repository: https://bitbucket.br-automation.com/projects/JUNF/repos/bnr-successor-product-finder/

Jira Project: https://jira.br-automation.com/projects/JUNF/summary

## Usage
### Updating the Application
Everytime the application starts, it will attempt to check the GitHub repository to see if there is a newer release version. If so, a message will appear asking if you would like to download the latest version. If the application is unable to establish a connection you will enter "Offline Mode" (see below). Answering "OK" will bring you to the direct download link for the zip file containing the release. If you answer "Cancel" you can still choose to update the application later by going to Options->About and clicking the "Download Update" button. If you already have the latest release version, "(Latest)" will appear next to you're version number and the "Download Update" button will be disabled.

![About Menu](assets/README/about%20menu.png)

### Lookup Process
Enter obsolete part numbers seperated by line. After clicking search the application will let you know the successor part(s), whether software changes are required, and if there are any notes on the obsolete product's successor. **Please make sure to always read the notes as they are often very important.** The "Successor Part Number(s)" and "Notes" boxes are both horizontally scrollable as their outputs often exceed the available space.

![Example Search](assets/README/example%20search%202.png)

### Themes
The theme of the application can be changed at any point via the Options->Theme menu. *Please note that not every theme has been individually tested.*

![Theme Menu](assets/README/theme%20menu.png)

### Offline Mode
If the application is unable to make a connection to the GitHub api upon startup, it will enter "Offline Mode". The only different between this state and normal operation is that in the "About" menu the "Download Update" button is disabled and "(Latest)" will not appear next to the version number even if it is the latest version.
