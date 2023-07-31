pyinstaller desktop_main.py -D --name effendi_desktop ^
    --add-data "ui/setup_dialog_v3.ui;ui" ^
    --add-data "ui/desktop_expandable.ui;ui" ^
    --add-data "ui/effendi_logo_v3.ico;ui" ^
    --add-data "ui/Backspace.png;ui" ^
    --add-data "ui/Copy.png;ui" ^
    --add-data "ui/Cut.png;ui" ^
    --add-data "ui/Paste.png;ui" ^
    --add-data "ui/Print.png;ui" ^
    --add-data "ui/Save.png;ui" ^
    --add-data "ui/Search.png;ui" ^
    --add-data "ui/Select_all.png;ui" ^
    --add-data "ui/Undo.png;ui" ^
    --add-data "ui/Update.png;ui" ^
    --add-data "ui/Hand_L.png;ui" ^
    --add-data "ui/Hand_R.png;ui" ^
    --add-data "dicts/English.txt;dicts" ^
    --add-data "dicts/German.txt;dicts" ^
    --add-data "personal_dicts;personal_dicts" ^
    --icon="ui/effendi_logo_v3.ico" ^
    --hidden-import=pkg_resources.py2_warn ^
    --hidden-import=pkg_resources.markers ^
    --hidden-import=tornado