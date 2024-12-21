#pragma once

#include "stdafx.h"
#include "resource.h"

#import <mscorlib.tlb> 
#import "TranslatorComp_Sundar.tlb" no_namespace named_guids

extern HINSTANCE	g_hInst;
extern HANDLE		g_hApplicationMutex;
extern DWORD		g_dwLastError;
extern BOOL			g_bStartSearchWindow;
extern HCURSOR		g_hCursorSearchWindow;
extern HCURSOR		g_hCursorPrevious;
extern HBITMAP		g_hBitmapFinderToolFilled;
extern HBITMAP		g_hBitmapFinderToolEmpty;
extern HWND			g_hwndFoundWindow;
extern HPEN			g_hRectanglePen;

#define WINDOW_FINDER_APP_MUTEX_NAME	"WINDOWFINDERMUTEX"
#define WM_START_SEARCH_WINDOW			WM_USER + 100
#define WINDOW_FINDER_TOOL_TIP			"Window Finder"

long StartSearchWindowDialog (HWND hwndMain);

BOOL CheckWindowValidity (HWND hwndDialog, HWND hwndToCheck);

long DoMouseMove 
(
  HWND hwndDialog, 
  UINT message, 
  WPARAM wParam, 
  LPARAM lParam
);

long DoMouseUp
(
  HWND hwndDialog, 
  UINT message, 
  WPARAM wParam, 
  LPARAM lParam
);



BOOL SetFinderToolImage (HWND hwndDialog, BOOL bSet);

BOOL MoveCursorPositionToBullsEye (HWND hwndDialog);

long SearchWindow (HWND hwndDialog);

long DisplayInfoOnFoundWindow (HWND hwndDialog, HWND hwndFoundWindow);

long RefreshWindow (HWND hwndWindowToBeRefreshed);

long HighlightFoundWindow (HWND hwndDialog, HWND hwndFoundWindow);

BOOL InitialiseResources();

void UninitialiseResources();

BOOL TranslateText(HWND hwndDialog);

BOOL CALLBACK SearchWindowDialogProc
(
  HWND hwndDlg, // handle to dialog box 
  UINT uMsg, // message 
  WPARAM wParam, // first message parameter 
  LPARAM lParam // second message parameter 
); 
