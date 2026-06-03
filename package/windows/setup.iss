[Setup]
AppId={{B5A31E7D-6C8E-4B07-9E1D-05F20E67142A}
AppName=Zesec
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\Zesec
DefaultGroupName=Zesec
OutputDir=..\..\dist
OutputBaseFilename=ZesecSetup
SetupIconFile=..\..\assets\icon\icon.ico
Compression=lzma2
SolidCompression=yes
#if Arch == "x64"
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
#endif

[Files]
Source: "..\..\build\zesec.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\build\zesec-gui.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Zesec"; Filename: "{app}\zesec-gui.exe"; Parameters: "--gui"
Name: "{autodesktop}\Zesec"; Filename: "{app}\zesec-gui.exe"; Parameters: "--gui"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\zesec-gui.exe"; Parameters: "--gui"; Description: "Launch Zesec"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCR; Subkey: ".zesec"; ValueType: string; ValueName: ""; ValueData: "Zesec.Document"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "Zesec.Document"; ValueType: string; ValueName: ""; ValueData: "Zesec Encrypted File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "Zesec.Document\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\zesec-gui.exe,0"
Root: HKCR; Subkey: "Zesec.Document\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\zesec-gui.exe"" --gui ""%1"""
