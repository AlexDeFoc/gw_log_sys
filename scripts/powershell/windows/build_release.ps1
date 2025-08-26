param (
  [string]$arch,
  [string]$compiler,
  [string]$link_type
)

$script_dir = $PSScriptRoot
$project_root = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($script_dir, '..', '..', '..'))
$output_dir = [System.IO.Path]::Combine($project_root, 'output')
$build_dir = [System.IO.Path]::Combine($project_root, 'build')

# Create output and build directories if they do not exist
if (-not (Test-Path $build_dir)) {
  New-Item -ItemType Directory -Path $build_dir | Out-Null
}
else {
  Remove-Item -Path $build_dir -Recurse -Force
  New-Item -ItemType Directory -Path $build_dir | Out-Null
}

if (-not (Test-Path $output_dir)) {
  New-Item -ItemType Directory -Path $output_dir | Out-Null
}

function GetResponse {
  param (
    [string]$question,
    [array]$options  # each item is [message, result]
  )
  Write-Host $question
  for ($i = 0; $i -lt $options.Length; $i++) {
    Write-Host "$($i + 1). $($options[$i][0])"
  }
  do {
    $ans = Read-Host "Enter choice (1-$($options.Length))"
  } until ($ans -match '^\d+$' -and [int]$ans -ge 1 -and [int]$ans -le $options.Length)
  return $options[[int]$ans - 1][1]
}

$cmake_configure_command = "cmake -S .. -B . -DBUILD_TESTS=OFF"
$cmake_build_command = "cmake --build ."

$include_dir = [System.IO.Path]::Combine($project_root, 'include')
$readme_filepath = [System.IO.Path]::Combine($project_root, 'README.md')
$license_filepath = [System.IO.Path]::Combine($project_root, 'LICENSE.md')
$changelog_filepath = [System.IO.Path]::Combine($project_root, 'change_log.md')

$lib_filepath = ''
$dll_filepath = ''

$platform = 'win'

if (-not $arch) {
  $arch = GetResponse "Choose architecture" @(
    @("64 bit", "x64"),
    @("32 bit", "x86")
  )
}

if ($arch -eq 'x64') {
  if ($compiler -ne 'msvc') {
    $cmake_configure_command += ' -DCMAKE_CXX_FLAGS="-m64"'
  }
  else {
    $cmake_configure_command += ' -A x64'
  }
}
else {
  if ($compiler -ne 'msvc') {
    $cmake_configure_command += ' -DCMAKE_CXX_FLAGS="-m32"'
  }
  else {
    $cmake_configure_command += ' -A Win32'
  }
}

if (-not $compiler) {
  $compiler = GetResponse "Choose compiler" @(
    @("Clang + Ninja", "clang_ninja"),
    @("GCC-MinGW + Ninja", "gcc_ninja"),
    @("MSVC", "msvc")
  )
}

switch ($compiler) {
  'clang_ninja' {
    $cmake_configure_command += ' -G "Ninja" -DCMAKE_CXX_COMPILER=clang++'
    $cmake_configure_command += ' -DCMAKE_BUILD_TYPE=Release'
    break
  }
  'gcc_ninja' {
    if ($arch -eq 'x64') {
      $cmake_configure_command += ' -G "Ninja" -DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-g++'
    }
    else {
      $cmake_configure_command += ' -G "Ninja" -DCMAKE_CXX_COMPILER=i686-w64-mingw32-g++'
    }
    $cmake_configure_command += ' -DCMAKE_BUILD_TYPE=Release'
    break
  }
  'msvc' {
    $cmake_configure_command += ' -G "Visual Studio 17 2022"'
    $cmake_build_command += ' --config Release'
    break
  }
}

if (-not $link_type) {
  $link_type = GetResponse "Choose link type" @(
    @("Static library", "static"),
    @("Dynamic library", "dynamic")
  )
}

switch ($link_type) {
  'static' {
    $cmake_configure_command += ' -DBUILD_STATIC_LIBRARY=ON'
    break
  }
  'dynamic' {
    $cmake_configure_command += ' -DBUILD_STATIC_LIBRARY=OFF'
    break
  }
}

Push-Location
Set-Location $build_dir
Invoke-Expression $cmake_configure_command
if (-not $?) {
  Pop-Location
  exit 1;
}

Invoke-Expression $cmake_build_command
if (-not $?) {
  Pop-Location
  exit 1;
}
Pop-Location

$files_to_copy = @(
  $readme_filepath,
  $license_filepath,
  $changelog_filepath,
  $include_dir
)

switch ($compiler) {
  'clang_ninja' {
    if ($link_type -eq 'static') {
      $lib_filepath = [System.IO.Path]::Combine($build_dir, 'gw_log_sys.lib')
      $files_to_copy += $lib_filepath
    }
    elseif ($link_type -eq 'dynamic') {
      $lib_filepath = [System.IO.Path]::Combine($build_dir, 'gw_log_sys.lib')
      $dll_filepath = [System.IO.Path]::Combine($build_dir, 'gw_log_sys.dll')
      $files_to_copy += $lib_filepath
      $files_to_copy += $dll_filepath
    }

    break
  }
  'gcc_ninja' {
    if ($link_type -eq 'static') {
      $lib_filepath = [System.IO.Path]::Combine($build_dir, 'libgw_log_sys.a')
      $files_to_copy += $lib_filepath
    }
    elseif ($link_type -eq 'dynamic') {
      $lib_filepath = [System.IO.Path]::Combine($build_dir, 'libgw_log_sys.dll.a')
      $dll_filepath = [System.IO.Path]::Combine($build_dir, 'libgw_log_sys.dll')
      $files_to_copy += $lib_filepath
      $files_to_copy += $dll_filepath
    }

    break
  }
  'msvc' {
    if ($link_type -eq 'static') {
      $lib_filepath = [System.IO.Path]::Combine($build_dir, 'Release', 'gw_log_sys.lib')
      $files_to_copy += $lib_filepath
    }
    elseif ($link_type -eq 'dynamic') {
      $lib_filepath = [System.IO.Path]::Combine($build_dir, 'Release', 'gw_log_sys.lib')
      $dll_filepath = [System.IO.Path]::Combine($build_dir, 'Release', 'gw_log_sys.dll')
      $files_to_copy += $lib_filepath
      $files_to_copy += $dll_filepath
    }

    break
  }
}

$release_name = @($platform, $arch, $compiler, $link_type) -join '__'

$release_dir = [System.IO.Path]::Combine($output_dir, $release_name)
if (-not(Test-Path($release_dir))) {
  New-Item -Path $release_dir -ItemType Directory | Out-Null
}
else {
  Remove-Item -Path $release_dir -Recurse -Force
  New-Item -Path $release_dir -ItemType Directory | Out-Null
}

foreach ($file in $files_to_copy) {
  Copy-Item -Path $file -Recurse -Destination $release_dir | Out-Null
}

$compressed_release_name = $release_name + '.zip'
$compressed_release_filepath = [System.IO.Path]::Combine($output_dir, $compressed_release_name)

if (Test-Path $compressed_release_filepath) {
  Remove-Item $compressed_release_filepath -Force
}

Compress-Archive -Path $release_dir -DestinationPath $compressed_release_filepath | Out-Null

Remove-Item -Path $release_dir -Recurse -Force