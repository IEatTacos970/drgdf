$inputs = @(
    "1",    # Artifact Multiplier
    "50",   # Research discount
    "3600", # mx_off
    "86400",# mxh_off
    "86400",# mxv_off
    "3600", # mx_off2
    "86400",# mxh_off2
    "86400",# mxv_off2
    "0",    # research sale
    "0",    # hab sale
    "0",    # vehicle sale
    "30",   # # of TE (forStart)
    "32",   # TE value when running single TE test (will be ignored for range run)
    "50",   # go until TE (for range run)
    "1",    # step
    "0"     # TIME_STEP (use event-driven)
)
$inputStr = $inputs -join "`n"

# Run range 30 to 50
$rangeInputFile = .\range_input.txt
$inputStr | Out-File -FilePath $rangeInputFile -Encoding utf8
$rangeOutput = Get-Content $rangeInputFile | & C:/Python312/python.exe .\simulator.py
$rangeOutput | Out-File -FilePath .\output_range.txt -Encoding utf8

# Now run single TE=32: we need to feed same inputs but set forStart=32 and go until 32
$inputs_single = $inputs[0..($inputs.Length-1)]
$inputs_single[11] = "32"  # set # of TE (forStart)
$inputs_single[12] = "32"  # go until TE
$inputStrSingle = $inputs_single -join "`n"
$singleInputFile = .\single_input.txt
$inputStrSingle | Out-File -FilePath $singleInputFile -Encoding utf8
$singleOutput = Get-Content $singleInputFile | & C:/Python312/python.exe .\simulator.py
$singleOutput | Out-File -FilePath .\output_single.txt -Encoding utf8

Write-Host "Ran both tests; outputs saved to output_range.txt and output_single.txt"