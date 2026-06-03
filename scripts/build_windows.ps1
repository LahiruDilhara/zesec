param (
    [string]$VERSION,
    [string]$ARCH
)

if (-not $VERSION) {
    Write-Error "VERSION parameter is required."
    exit 1
}

New-Item -ItemType Directory -Force -Path dist | Out-Null

Write-Host "Packaging for Windows (VERSION: $VERSION, ARCH: $ARCH)"

$isccArch = if ($ARCH -eq 'amd64') { 'x64' } else { 'x86' }
$wixPlatform = if ($ARCH -eq 'amd64') { 'x64' } else { 'x86' }
$win64Attr = if ($ARCH -eq 'amd64') { "Win64='yes'" } else { "" }
$progFilesId = if ($ARCH -eq 'amd64') { 'ProgramFiles64Folder' } else { 'ProgramFilesFolder' }

# Compile Inno Setup for .exe installer
& "C:\Program Files (x86)\Inno Setup 6\iscc.exe" "/DMyAppVersion=$VERSION" "/DArch=$isccArch" "package\windows\setup.iss"
if (Test-Path "dist\ZesecSetup.exe") {
    Move-Item -Path "dist\ZesecSetup.exe" -Destination "dist\Zesec_${VERSION}_Windows_${ARCH}_Setup.exe" -Force
}

# Build a WiX MSI with gui launch shortcut
$wixFile = "package\windows\setup.wxs"
Set-Content -Path $wixFile -Value @"
<?xml version='1.0' encoding='windows-1252'?>
<Wix xmlns='http://schemas.microsoft.com/wix/2006/wi'>
  <Product Name='Zesec' Id='*' UpgradeCode='B5A31E7D-6C8E-4B07-9E1D-05F20E67142A' Language='1033' Codepage='1252' Version='$VERSION' Manufacturer='Lahiru Dilhara'>
    <Package Id='*' Platform='$wixPlatform' Keywords='Installer' Description='Zesec Installer' Manufacturer='Lahiru Dilhara' InstallerVersion='200' Languages='1033' Compressed='yes' SummaryCodepage='1252' />
    <MajorUpgrade DowngradeErrorMessage='A newer version of Zesec is already installed.' />
    <Media Id='1' Cabinet='Zesec.cab' EmbedCab='yes' DiskPrompt='CD-ROM #1' />
    <Property Id='DiskPrompt' Value='Zesec Installation [1]' />
    
    <Icon Id="icon.ico" SourceFile="assets\icon\icon.ico"/>
    <Property Id="ARPPRODUCTICON" Value="icon.ico" />
    
    <Directory Id='TARGETDIR' Name='SourceDir'>
      <Directory Id='$progFilesId' Name='PFiles'>
        <Directory Id='INSTALLDIR' Name='Zesec'>
          <Component Id='MainExecutable' Guid='*' $win64Attr>
            <File Id='ZesecEXE' Name='main.exe' DiskId='1' Source='main.exe' KeyPath='yes'/>
          </Component>
        </Directory>
      </Directory>
      <Directory Id='ProgramMenuFolder'>
        <Component Id='ApplicationShortcut' Guid='*'>
          <Shortcut Id='ApplicationStartMenuShortcut' Name='Zesec' Target='[INSTALLDIR]main.exe' Arguments='--gui' WorkingDirectory='INSTALLDIR' Icon='icon.ico'/>
          <RegistryValue Root='HKCU' Key='Software\LahiruDilhara\Zesec' Name='installed' Type='integer' Value='1' KeyPath='yes'/>
        </Component>
      </Directory>
      <Directory Id='DesktopFolder'>
        <Component Id='DesktopShortcut' Guid='*'>
          <Shortcut Id='ApplicationDesktopShortcut' Name='Zesec' Target='[INSTALLDIR]main.exe' Arguments='--gui' WorkingDirectory='INSTALLDIR' Icon='icon.ico'/>
          <RegistryValue Root='HKCU' Key='Software\LahiruDilhara\Zesec' Name='desktop' Type='integer' Value='1' KeyPath='yes'/>
        </Component>
      </Directory>
    </Directory>
    <Feature Id='Complete' Level='1'>
      <ComponentRef Id='MainExecutable' />
      <ComponentRef Id='ApplicationShortcut' />
      <ComponentRef Id='DesktopShortcut' />
    </Feature>
  </Product>
</Wix>
"@

& candle.exe $wixFile -out package\windows\setup.wixobj
& light.exe -ext WixUIExtension package\windows\setup.wixobj -out "dist\Zesec_${VERSION}_Windows_${ARCH}_Setup.msi"
