##About this tool##

The consumer product I am working on was tested in different languages of Windows. As a non-Reader of that language, I 
found it difficult to understand what to click and how to manoeuvre. It gets tougher for RTL languages such as Hebrew and 
Arabic.

This tool takes an inspiration from Microsoft SPY++ tool. The user can move the "Bulls Eye" to the text he is not able
to understand. The tool get the translation for the text in English (uses Bing Translate)

![alt text](https://github.com/clicksuku/SundarkpCode/blob/master/Images/SPY%20Translate.png "Tool Snapshot")


##Few more details##

  1. **Why Bing Translate?**
     Bing supports free translation for first 20 million characters.
  2. **Design**
     Win32 Application uses ‘WindowFromPoint’ to get the window on the curson position. GetWindowText to get the text. 
     (PostMessage). Translate calls C# component (registered as COM). C# component uses Bing API to translate text.
     
##Steps to Install##

###Pre-Requisites###
  
1. Microsoft Dotnet Framework 4.0
2. [Microsoft Visual C++ 2010 Redistributable Package x86](http://www.microsoft.com/en-us/download/details.aspx?id=5555)

###Installation###
  
1. From the location “C:\Windows\Microsoft.NET\Framework\v4.0.30319” , run the following command 
   to register the COM component 
         *Regasm.exe “<Tool Copy Location>\TranslatorComp.dll” /tlb: “<Tool Copy Location>\TranslatorComp.tlb” /codebase*
         
2. Run FindControl.exe
3. Move the bulls eye to any window to capture text. Or you can copy text directly into the Source text box.
     
##Demo##

<a href="http://www.youtube.com/watch?feature=player_embedded&v=vHyN0FkzYnk" target="_blank">
<img src="http://img.youtube.com/vi/vHyN0FkzYnk/0.jpg" alt="https://www.youtube.com/watch?v=vHyN0FkzYnk" width="240" height="180" border="10" /></a>


##Limitations##

20 Million characters translation limit in Bing API

#License#
New APACHE License - Copyright(c) 2014, Sundara Kumar Padmanabhan. 
See [License](http://www.apache.org/licenses/LICENSE-2.0.html) for details.

    
##References##

     1. http://www.codeproject.com/Articles/1698/MS-Spy-style-Window-Finder
     2.	Bing Translator - http://msdn.microsoft.com/en-us/library/dd576287.aspx
     
     
