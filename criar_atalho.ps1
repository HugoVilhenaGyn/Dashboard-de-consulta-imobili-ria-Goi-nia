$WS = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath('Desktop')
$SC = $WS.CreateShortcut("$Desktop\Cadastro Imobiliário.lnk")
$SC.TargetPath = 'wscript.exe'
$SC.Arguments = '"c:\VS Code\upload_supabase.py\iniciar_silencioso.vbs"'
$SC.WorkingDirectory = 'c:\VS Code\upload_supabase.py'
$SC.Description = 'Abrir Cadastro Imobiliário Goiânia'
$SC.IconLocation = 'c:\VS Code\upload_supabase.py\icon.ico,0'
$SC.Save()
Write-Host 'Atalho atualizado com icone personalizado!'
