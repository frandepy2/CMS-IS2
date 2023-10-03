del /s /q var
for /d %%i in (cmsis2\*) do (
    del /s /q "%%i\migrations"
)
