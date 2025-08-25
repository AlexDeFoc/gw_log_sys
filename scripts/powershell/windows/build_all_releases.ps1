$script_dir = $PSScriptRoot
$build_script_path = [System.IO.Path]::Combine($script_dir, 'build_release.ps1')

$compilers = @('clang_ninja', 'gcc_ninja', 'msvc')
$architectures = @('x64', 'x86')
$link_types = @('static', 'dynamic')

$total = $compilers.Count * $architectures.Count * $link_types.Count
$count = 1

foreach ($c in $compilers) {
  foreach ($a in $architectures) {
    foreach ($l in $link_types) {
      Write-Host "Building [$count/$total] $c $a $l ..." -ForegroundColor Cyan
      & powershell -ExecutionPolicy Bypass -File $build_script_path -compiler $c -arch $a -link_type $l
      if (-not $?) {
        Write-Host "Build failed at [$count/$total] $c $a $l. Exiting." -ForegroundColor Red
        exit 1
      }
      $count++
    }
  }
}

Write-Host "FINISHED" -ForegroundColor Green