// SampleWinApp.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "ControlFinder.h"
#include <atlstr.h>


#define MAX_LOADSTRING 100
#define BULLSEYE_CENTER_X_OFFSET		15
#define BULLSEYE_CENTER_Y_OFFSET		18

HINSTANCE	g_hInst = NULL;
BOOL		g_bStartSearchWindow = FALSE;
HCURSOR		g_hCursorSearchWindow = NULL;
HCURSOR		g_hCursorPrevious = NULL;
HBITMAP		g_hBitmapFinderToolFilled;
HBITMAP		g_hBitmapFinderToolEmpty;
HWND		g_hwndFoundWindow = NULL;
HPEN		g_hRectanglePen = NULL;
HPEN		g_hPrevPen = NULL;   // Handle of the existing pen in the DC of the found window.
HBRUSH		g_hPrevBrush = NULL; // Handle of the existing brush in the DC of the found window.




int APIENTRY _tWinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPTSTR    lpCmdLine,
                     int       nCmdShow)
{

	MSG		msg;
	long lRet = 0;
	g_hInst = hInstance;

	BOOL bRet = InitialiseResources();
	if (bRet == FALSE)
	{
		UninitialiseResources();
		return lRet;
	}

	HWND hDialog = CreateDialog
	(
		(HINSTANCE)g_hInst, // handle to application instance 
		(LPCTSTR)MAKEINTRESOURCE(IDD_SEARCH_WINDOW), // identifies dialog box template 
		NULL, // handle to owner window 
		(DLGPROC)SearchWindowDialogProc // pointer to dialog box procedure 
	);

	ShowWindow(hDialog, SW_SHOWNORMAL);
	UpdateWindow(hDialog);

	while (GetMessage(&msg, (HWND)NULL, 0, 0)) 
	{ 
		if (!TranslateAccelerator(hDialog, NULL, &msg))
		{ 
			TranslateMessage(&msg); 
			DispatchMessage(&msg); 
		} 
	}

	lRet = msg.wParam;
	return lRet;
}


BOOL InitialiseResources()
{
	  BOOL bRet = FALSE;

	  g_hCursorSearchWindow = LoadCursor (g_hInst, MAKEINTRESOURCE(IDC_CURSOR_SEARCH_WINDOW));
	  g_hRectanglePen = CreatePen (PS_SOLID, 3, RGB(0, 0, 255));
	  //g_hRectanglePen = CreatePen (PS_SOLID, 3, RGB(256, 0, 0));
	  g_hBitmapFinderToolFilled = LoadBitmap (g_hInst, MAKEINTRESOURCE(IDB_BITMAP_FINDER_FILLED));
	  g_hBitmapFinderToolEmpty = LoadBitmap (g_hInst, MAKEINTRESOURCE(IDB_BITMAP_FINDER_EMPTY));

	  if ((g_hCursorSearchWindow == NULL) || (g_hRectanglePen == NULL) || (g_hBitmapFinderToolFilled == NULL) || (g_hBitmapFinderToolEmpty == NULL))
	  {
		return FALSE;	
	  }

	  return TRUE;
}

void UninitialiseResources()
{    
	if (g_hRectanglePen)
	{
		DeleteObject (g_hRectanglePen);
		g_hRectanglePen = NULL;
	}

	if (g_hPrevPen)
	{
		DeleteObject (g_hPrevPen);
		g_hPrevPen = NULL;
	}

	if (g_hBitmapFinderToolFilled)
	{
		DeleteObject (g_hBitmapFinderToolFilled);
		g_hBitmapFinderToolFilled = NULL;
	}

	if (g_hBitmapFinderToolEmpty)
	{
		DeleteObject (g_hBitmapFinderToolEmpty);
		g_hBitmapFinderToolEmpty = NULL;
	}  
}


BOOL CALLBACK SearchWindowDialogProc
(
  HWND hwndDlg, // handle to dialog box 
  UINT uMsg, // message 
  WPARAM wParam, // first message parameter 
  LPARAM lParam // second message parameter 
)
{
		BOOL bRet = FALSE;  // Default return value.

		switch (uMsg)
		{
			case WM_INITDIALOG :
				bRet = TRUE;
				break;
			case WM_MOUSEMOVE :
			{
				bRet = TRUE;			
				if (g_bStartSearchWindow)
				{
					// Only when we have started the Window Searching operation will we 
					// track mouse movement.
					DoMouseMove(hwndDlg, uMsg, wParam, lParam);
				}
				break;
			}
			case WM_LBUTTONUP :
			{
				bRet = TRUE;
				if (g_bStartSearchWindow)
				{
					// Only when we have started the window searching operation will we
					// be interested when the user lifts up the left mouse button.
					DoMouseUp(hwndDlg, uMsg, wParam, lParam);
				}
				break;
			}			
			case WM_COMMAND :
			{
				WORD wNotifyCode = HIWORD(wParam); // notification code 
				WORD wID = LOWORD(wParam);         // item, control, or accelerator identifier 
				HWND hwndCtl = (HWND)lParam;      // handle of control 

				if ((wID == IDOK) || (wID == IDCANCEL))
				{
					bRet = TRUE;
					UninitialiseResources();
					PostQuitMessage(0);
					break;
				}
				
				if (wID == IDC_STATIC_ICON_FINDER_TOOL)
				{
					// Because the IDC_STATIC_ICON_FINDER_TOOL static control is set with the SS_NOTIFY
					// flag, the Search Window's dialog box will be sent a WM_COMMAND message when this 
					// static control is clicked.
					bRet = TRUE;
					// We start the window search operation by calling the DoSearchWindow() function.
					SearchWindow(hwndDlg);
					break;
				}

				if (wID == IDTRANSLATE)
				{					
					TranslateText(hwndDlg);
					break;
				}

				break;
			}
			case WM_DESTROY:
			{
				UninitialiseResources();
				PostQuitMessage(0);
				return 1;
			}
			case WM_CLOSE:
			{				
				UninitialiseResources();
				PostQuitMessage(0);
				return 1;
			}	
			default :
			{
				DefWindowProc
				(
					(HWND)hwndDlg, // handle to main frame window 
					(UINT)uMsg, // message 
					(WPARAM)wParam, // first message parameter 
					(LPARAM)lParam // second message parameter 
				); 

				bRet = FALSE;
				break;
			}
		}
		return bRet;
}


// Synopsis :
// 1. This function checks a hwnd to see if it is actually the "Search Window" Dialog's or Main Window's
// own window or one of their children. If so a FALSE will be returned so that these windows will not
// be selected. 
//
// 2. Also, this routine checks to see if the hwnd to be checked is already a currently found window.
// If so, a FALSE will also be returned to avoid repetitions.
BOOL CheckWindowValidity (HWND hwndDialog, HWND hwndToCheck)
{
	HWND hwndTemp = NULL;	

	// The window must not be NULL.
	// It must also be a valid window as far as the OS is concerned.
	// Ensure that the window is not the current one which has already been found.
	// It also must not be the "Search Window" dialog box itself.

	if ((hwndToCheck == NULL) ||(IsWindow(hwndToCheck) == FALSE) || 
			(hwndToCheck == g_hwndFoundWindow) || (hwndToCheck == hwndDialog))
	{
		return FALSE;
	}
			
	
	// It also must not be one of the dialog box's children...
	hwndTemp = GetParent (hwndToCheck);
	if ((hwndTemp == hwndDialog))
	{
		return FALSE;
	}

	return TRUE;
}



// Synopsis :
// 1. This is the handler for WM_MOUSEMOVE messages sent to the "Search Window" dialog proc.
//
// 2. Note that we do not handle every WM_MOUSEMOVE message sent. Instead, we check to see 
// if "g_bStartSearchWindow" is TRUE. This BOOL will be set to TRUE when the Window
// Searching Operation is actually started. See the WM_COMMAND message handler in 
// SearchWindowDialogProc() for more details.
//
// 3. Because the "Search Window" dialog immediately captures the mouse when the Search Operation 
// is started, all mouse movement is monitored by the "Search Window" dialog box. This is 
// regardless of whether the mouse is within or without the "Search Window" dialog. 
//
// 4. One important note is that the horizontal and vertical positions of the mouse cannot be 
// calculated from "lParam". These values can be inaccurate when the mouse is outside the
// dialog box. Instead, use the GetCursorPos() API to capture the position of the mouse.
long DoMouseMove 
(
  HWND hwndDialog, 
  UINT message, 
  WPARAM wParam, 
  LPARAM lParam
)
{
	POINT		screenpoint;
	HWND		hwndFoundWindow = NULL;
	TCHAR		szText[256];
	long		lRet = 0;

	// Must use GetCursorPos() instead of calculating from "lParam".
	GetCursorPos (&screenpoint);  

	// Display global positioning in the dialog box.
	wsprintf (szText, L"%d", screenpoint.x);
	SetDlgItemText (hwndDialog, IDC_STATIC_X_POS, szText);
  
	wsprintf (szText, L"%d", screenpoint.y);
	SetDlgItemText (hwndDialog, IDC_STATIC_Y_POS, szText);

	// Determine the window that lies underneath the mouse cursor.
	hwndFoundWindow = WindowFromPoint (screenpoint);

	// Check first for validity.
	if (CheckWindowValidity (hwndDialog, hwndFoundWindow))
	{
		// We have just found a new window.
		// Display some information on this found window.
		DisplayInfoOnFoundWindow (hwndDialog, hwndFoundWindow);

		// If there was a previously found window, we must instruct it to refresh itself. 
		// This is done to remove any highlighting effects drawn by us.
		if (g_hwndFoundWindow)
		{
			//DeselectWindow(g_hwndFoundWindow);
			RefreshWindow (g_hwndFoundWindow);
		}

		// Indicate that this found window is now the current global found window.
		g_hwndFoundWindow = hwndFoundWindow;

		// We now highlight the found window.

		//HighlightFoundWindow (hwndDialog, g_hwndFoundWindow);
	}

	return lRet;
}





// Synopsis :
// 1. Handler for WM_LBUTTONUP message sent to the "Search Window" dialog box.// 
// 2. We restore the screen cursor to the previous one.//
// 3. We stop the window search operation and release the mouse capture.

long DoMouseUp
(
  HWND hwndDialog, 
  UINT message, 
  WPARAM wParam, 
  LPARAM lParam
)
{
	long lRet = 0;

	// If we had a previous cursor, set the screen cursor to the previous one.
	// The cursor is to stay exactly where it is currently located when the 
	// left mouse button is lifted.
	if (g_hCursorPrevious)
	{
		SetCursor (g_hCursorPrevious);
	}

	// If there was a found window, refresh it so that its highlighting is erased. 
	if (g_hwndFoundWindow)
	{
		RefreshWindow (g_hwndFoundWindow);
	}

	// Set the bitmap on the Finder Tool icon to be the bitmap with the bullseye bitmap.
	SetFinderToolImage (hwndDialog, TRUE);
	// Very important : must release the mouse capture.
	ReleaseCapture ();

	// Set the global search window flag to FALSE.
	g_bStartSearchWindow = FALSE;
	return lRet;
}




// Synopsis :
// 1. This routine sets the Finder Tool icon to contain an appropriate bitmap.
//
// 2. If bSet is TRUE, we display the BullsEye bitmap. Otherwise the empty window
// bitmap is displayed.
BOOL SetFinderToolImage (HWND hwndDialog, BOOL bSet)
{
	HBITMAP hBmpToSet = NULL;
	BOOL bRet = TRUE;

	if (bSet)
	{
		// Set a FILLED image.
		hBmpToSet = g_hBitmapFinderToolFilled;
	}
	else
	{
		// Set an EMPTY image.
		hBmpToSet = g_hBitmapFinderToolEmpty;
	}

	SendDlgItemMessage
	(
		(HWND)hwndDialog, // handle of dialog box 
		(int)IDC_STATIC_ICON_FINDER_TOOL, // identifier of control 
		(UINT)STM_SETIMAGE, // message to send 
		(WPARAM)IMAGE_BITMAP, // first message parameter 
		(LPARAM)hBmpToSet // second message parameter 
	);

	return bRet;
}



// Synopsis :
// 1. This routine moves the mouse cursor hotspot to the exact 
// centre position of the bullseye in the finder tool static control.
//
// 2. This function, when used together with DoSetFinderToolImage(),
// gives the illusion that the bullseye image has indeed been transformed
// into a cursor and can be moved away from the Finder Tool Static
// control.
BOOL MoveCursorPositionToBullsEye (HWND hwndDialog)
{
	BOOL bRet = FALSE;
	HWND hwndToolFinder = NULL;
	RECT rect;
	POINT screenpoint;

	// Get the window handle of the Finder Tool static control.
	hwndToolFinder = GetDlgItem (hwndDialog, IDC_STATIC_ICON_FINDER_TOOL);
	if (hwndToolFinder)
	{
		// Get the screen coordinates of the static control,
		// add the appropriate pixel offsets to the center of 
		// the bullseye and move the mouse cursor to this exact
		// position.
		GetWindowRect (hwndToolFinder, &rect);
		screenpoint.x = rect.left + BULLSEYE_CENTER_X_OFFSET;
		screenpoint.y = rect.top + BULLSEYE_CENTER_Y_OFFSET;
		SetCursorPos (screenpoint.x, screenpoint.y);
	}

	return bRet;
}





// Synopsis :
// 1. This function starts the window searching operation.
//
// 2. A very important part of this function is to capture 
// all mouse activities from now onwards and direct all mouse 
// messages to the "Search Window" dialog box procedure.
long SearchWindow (HWND hwndDialog)
{
	long lRet = 0;

	// Set the global "g_bStartSearchWindow" flag to TRUE.
	g_bStartSearchWindow = TRUE;
	// Display the empty window bitmap image in the Finder Tool static control.
	SetFinderToolImage (hwndDialog, FALSE);
	MoveCursorPositionToBullsEye (hwndDialog);
	// Set the screen cursor to the BullsEye cursor.
	if (g_hCursorSearchWindow)
	{
		g_hCursorPrevious = SetCursor (g_hCursorSearchWindow);
	}
	else
	{
		g_hCursorPrevious = NULL;
	}

	// Very important : capture all mouse activities from now onwards and
	// direct all mouse messages to the "Search Window" dialog box procedure.
	SetCapture (hwndDialog);    
	return lRet;
}



long DisplayInfoOnFoundWindow (HWND hwndDialog, HWND hwndFoundWindow)
{
	RECT		rect;              // Rectangle area of the found window.
	const		int bufferSize = 1024;		
	TCHAR		szWindowText[bufferSize] = _T("");
	long		lRet = 0;

	// Get the screen coordinates of the rectangle of the found window.
	GetWindowRect (hwndFoundWindow, &rect);

	//Get Text from Window
	int textLen = (int)SendMessage(hwndFoundWindow, WM_GETTEXTLENGTH, 0, 0);

	if(0 < textLen)
	{		
		SendMessage(hwndFoundWindow, WM_GETTEXT, (WPARAM)bufferSize, (LPARAM)szWindowText);		
	}
	
	
	// Display some information on the found window.	
	SetDlgItemText (hwndDialog, IDC_EDIT_SOURCE_TEXT, szWindowText);
	memset(szWindowText,'\0',sizeof(szWindowText));

	return lRet;
}





long RefreshWindow (HWND hwndWindowToBeRefreshed)
{
	long lRet = 0;		
	RECT		rect;              // Rectangle area of the found window.
	
	// Get the screen coordinates of the rectangle of the found window.
	GetWindowRect (hwndWindowToBeRefreshed, &rect);
	//InvalidateRect (hwndWindowToBeRefreshed, NULL, NULL);
	//UpdateWindow (hwndWindowToBeRefreshed);
	lRet =  RedrawWindow (hwndWindowToBeRefreshed, &rect, NULL,  RDW_INVALIDATE | RDW_UPDATENOW | RDW_ALLCHILDREN);
	return lRet;
}




// Performs a highlighting of a found window.
// Comments below will demonstrate how this is done.
long HighlightFoundWindow (HWND hwndDialog, HWND hwndFoundWindow)
{
	HDC		hWindowDC = NULL;  // The DC of the found window.	
	RECT		rect;              // Rectangle area of the found window.
	long		lRet = 0;

	// Get the screen coordinates of the rectangle of the found window.
	GetWindowRect (hwndFoundWindow, &rect);

	// Get the window DC of the found window.
	hWindowDC = GetWindowDC (hwndFoundWindow);

	if (hWindowDC)
	{
		// Select our created pen into the DC and backup the previous pen.
		g_hPrevPen = (HPEN) SelectObject (hWindowDC, g_hRectanglePen);
		// Select a transparent brush into the DC and backup the previous brush.
		g_hPrevBrush = (HBRUSH) SelectObject (hWindowDC, GetStockObject(HOLLOW_BRUSH));
		// Draw a rectangle in the DC covering the entire window area of the found window.
		Rectangle (hWindowDC, 0, 0, rect.right - rect.left, rect.bottom - rect.top);		

		SelectObject (hWindowDC, g_hPrevPen);
		SelectObject (hWindowDC, g_hPrevBrush);

		// Finally release the DC.
		ReleaseDC (hwndFoundWindow, hWindowDC);
	}
	
	return lRet;
}


//Calls C# COM component which calls the Bing translator API
//Translates input text to output

BOOL TranslateText(HWND hwndDlg)
{
	CoInitialize(NULL);
	
	BOOL bRet = TRUE;						
	TCHAR szText[2048];	

	SetDlgItemText (hwndDlg, IDC_EDIT_TRANSLATED_TEXT, _T("Translating Message.....") );

	GetDlgItemText(hwndDlg, IDC_EDIT_SOURCE_TEXT, szText, 1024);
	
	CString strToTranslate(szText);
	strToTranslate.Replace(_T("&"), _T(""));

	CComPtr<ITranslator> cpi = NULL; 
	TCHAR szTranslated[2048];

	HRESULT hr = CoCreateInstance(CLSID_TranslatorServiceComp,
				NULL, CLSCTX_INPROC_SERVER,
				IID_ITranslator, reinterpret_cast<void**>(&cpi));

	if (FAILED(hr))
	{
		printf("Couldn't create the instance!... 0x%x\n", hr);
	}

	

	_bstr_t strTranslatedText = cpi->Translate(_bstr_t(strToTranslate));   				
	_stprintf(szTranslated, _T("%s"), (LPCTSTR)strTranslatedText);	

	MessageBox(NULL, szTranslated , L"Test", MB_OK);
	SetDlgItemText (hwndDlg, IDC_EDIT_TRANSLATED_TEXT, szTranslated );

	CoUninitialize();
	return bRet;
}