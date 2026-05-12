$ErrorActionPreference = "Stop"

$taskName = "TVS Rotator"
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$cmdPath = Join-Path $projectDir "run_tv_rotator.cmd"

if (-not (Test-Path $cmdPath)) {
    throw "No se encontro el archivo: $cmdPath"
}

$action = New-ScheduledTaskAction `
    -Execute $cmdPath `
    -WorkingDirectory $projectDir

$trigger = New-ScheduledTaskTrigger -AtLogOn

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -MultipleInstances IgnoreNew `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Inicia el rotador TVS en modo kiosco al iniciar sesion." `
    -Force | Out-Null

Write-Host "Tarea creada o actualizada: $taskName"
Write-Host "Comando: $cmdPath"
