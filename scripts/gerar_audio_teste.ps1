$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $speaker.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::NotSet,[System.Speech.Synthesis.VoiceAge]::NotSet,0,[System.Globalization.CultureInfo]::GetCultureInfo('pt-BR'))
    $speaker.SetOutputToWaveFile((Join-Path (Get-Location) 'data\samples\fala-sintetica.wav'))
    $speaker.Speak('Durante o exercício eu senti dor no braço. Agora estou melhor.')
} finally {
    $speaker.Dispose()
}
