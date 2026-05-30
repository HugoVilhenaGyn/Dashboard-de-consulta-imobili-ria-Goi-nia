$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath('Desktop')
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Dashboard Imoveis.lnk")
$Shortcut.TargetPath = "c:\VS Code\upload_supabase.py\run_dashboard.bat"
$Shortcut.WorkingDirectory = "c:\VS Code\upload_supabase.py"
$Shortcut.IconLocation = "shell32.dll,43"
$Shortcut.Save()
